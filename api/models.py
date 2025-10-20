from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    edited = models.BooleanField(default=False)
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    PRIORITY_LOW = 'low'
    PRIORITY_MED = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MED, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MED)
    in_calendar = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.scheduled_date:
            return f"{self.name} ({self.scheduled_date}) [{self.priority}]"
        return self.name
    