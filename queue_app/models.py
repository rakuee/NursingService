from django.db import models

# Create your models here.

class Queue(models.Model):
    role_choices = [
        ('student', 'Student'),
        ('worker', 'Worker'),
    ] 

    status_choices = [
        ('waiting', 'Waiting'),
        ('attending', 'Attending'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=role_choices)
    join_time = models.DateTimeField(auto_now_add=True)
    attended_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices)
