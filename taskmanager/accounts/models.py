from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    members = models.ManyToManyField(User)
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='team_created_by')

    def __str__(self):
        return self.team_name

    class Meta:
        ordering = ('team_name',)
