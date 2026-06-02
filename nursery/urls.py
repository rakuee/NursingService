from django.urls import path
from . import views

urlpatterns = [
    path('users', views.create_user, name='create_user'),
    path('users/<int:user_id>', views.get_user, name='get_user'),
    path('queue', views.get_queue, name='get_queue'),
    path('queue/<int:user_id>', views.get_queue_entry, name='get_queue_entry'),
    path('queue/attend', views.attend, name='attend'),
    path('logs/<int:user_id>', views.get_logs, name='get_logs'),
    path('stats/peak-hours', views.peak_hours, name='peak_hours'),
]