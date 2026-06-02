from rest_framework import serializers
from .models import User, QueueEntry, Log

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'role_type', 'created_at']

class QueueEntrySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = QueueEntry
        fields = ['id', 'user_id', 'user_name', 'status', 'joined_at', 'attended_at']

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'user_id', 'joined_at', 'attended_at', 'wait_time']