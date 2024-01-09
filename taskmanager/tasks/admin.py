from django.contrib import admin

# Register your models here.
from .models import Task, Comment

admin.site.register(Task)
admin.site.register(Comment)
