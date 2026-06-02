from django.shortcuts import render
from django.utils import timezone
from django.db.models import Avg
from django.db.models.functions import ExtractHour
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, QueueEntry, Log
from .serializers import UserSerializer, QueueEntrySerializer, LogSerializer

# Create your views here.

def home(request):
    return render(request, 'home.html')

# POST /api/users/
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        QueueEntry.objects.create(user=user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /api/users/{id}
@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)

# GET /api/queue/
@api_view(['GET'])
def get_queue(request):
    entries = QueueEntry.objects.filter(status='waiting')
    return Response(QueueEntrySerializer(entries, many=True).data)

# GET /api/users/{user_id}
@api_view(['GET'])
def get_queue_entry(request, user_id):
    try:
        entry = QueueEntry.objects.filter(user_id=user_id, status='waiting').latest('joined_at')
    except QueueEntry.DoesNotExist:
        return Response({'detail': 'Not in queue'}, status=status.HTTP_404_NOT_FOUND)
    return Response(QueueEntrySerializer(entry).data)

# POST /api/queue/attend
@api_view(['POST'])
def attend(request):
    user_id = request.data.get('user_id')
    try:
        entry = QueueEntry.objects.filter(user_id=user_id, status='waiting').latest('joined_at')
    except QueueEntry.DoesNotExist:
        return Response({'detail': 'Not in queue'}, status=status.HTTP_404_NOT_FOUND)
    
    now = timezone.now()
    entry.status = 'done'
    entry.attended_at = now
    entry.save()

    wait = round((now - entry.joined_at).total_seconds() / 60, 1)
    Log.objects.create(
        user=entry.user,
        entry=entry,
        joined_at=entry.joined_at,
        attended_at=now,
        wait_time=wait,
    )

    return Response(QueueEntrySerializer(entry).data)

# GET /api/logs/{user_id}
@api_view(['GET'])
def get_logs(request, user_id):
    logs = Log.objects.filter(user_id=user_id).order_by('-joined_at')
    return Response(LogSerializer(logs, many=True).data)

# GET /api/stats/peak-hours
@api_view(['GET'])
def peak_hours(request):
    stats = (
        Log.objects
        .annotate(hour=ExtractHour('joined_at'))
        .values('hour')
        .annotate(avg_wait=Avg('wait_minutes'))
        .order_by('hour')
    )
    data = [{'hour': f"{r['hour']}:00", 'avg_wait_minutes': round(r['avg_wait'], 1)} for r in stats]
    return Response(data)