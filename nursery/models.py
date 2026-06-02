from django.db import models

# Create your models here.

class User(models.Model):
    role_choices = [
        ('student', 'Student'),
        ('worker', 'Worker'),
    ]

    name = models.CharField(max_length=100)
    role_type = models.CharField(max_length=10, choices=role_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role_type})"

class QueueEntry(models.Model):
    status_choices = [
        ('waiting', 'Waiting'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices, default='waiting')
    joined_at = models.DateTimeField(auto_now_add=True)
    attended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.user.name} - {self.status}"
    
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(QueueEntry, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    attended_at = models.DateTimeField(null=True, blank=True)
    wait_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.entry.status}, Wait Time: {self.wait_time}"