from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Team

class Task(models.Model):
    STATUS_CHOICES = (
        ('Planned', 'Planned'),
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done')
    )

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_date = models.DateField(default=timezone.now, blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, related_name='task_created_by', on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(User, related_name='task_assigned_to')
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    files = models.FileField(upload_to='task_files/', blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    body = models.TextField()
    file = models.FileField(upload_to='comment_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
