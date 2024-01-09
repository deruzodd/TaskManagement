from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Task, Comment
from tasks.models import Team
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
import os

@csrf_exempt
@login_required(login_url='accounts:login')
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        assignees = request.POST.getlist('assignee')
        files = request.FILES.get('files')

        task = Task(title=title, description=description, status=status, created_by=request.user, files=files)

        team_id = request.POST.get('team_id', None)

        if team_id is not None:
            try:
                team = Team.objects.get(pk=team_id)
                task.team = team
            except Team.DoesNotExist:
                return redirect('accounts:home')

        task.save()

        if len(assignees) == 0:
            task.assigned_to.add(request.user)

        for assignee in assignees:
            task.assigned_to.add(User.objects.get(username=assignee))

        task.save()

        if team_id is not None:
            return redirect('accounts:team_detail', team_id=team_id)

        return redirect('accounts:home')

    users = User.objects.all()

    return render(request, 'create.html', {'users': users})

@csrf_exempt
@login_required(login_url='accounts:login')
def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return redirect('accounts:home')

    team = task.team

    if team is None:
        if request.user != task.created_by and request.user not in task.assigned_to.all():
            messages.error(request, "You can't view this task")
            return redirect('accounts:home')
    else:
        if request.user not in team.members.all():
            messages.error(request, "You can't view this task")
            return redirect('accounts:home')

    users = User.objects.all()

    comments = Comment.objects.filter(task=task)

    statuses = ['Planned', 'Ongoing', 'Done']

    return render(request, "detail.html", {
        "id": task_id, "task": task,
        "users": users, "statuses": statuses,
        "comments": comments
    })

@csrf_exempt
@login_required(login_url='accounts:login')
def edit(request):
    if request.method == 'POST':
        try:
            task = Task.objects.get(pk=request.POST.get("task_id"))
        except Task.DoesNotExist:
            messages.error(request, "Task not found")
            return redirect('accounts:home')

        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        assignees = request.POST.getlist('assignee')

        task.title = title
        task.description = description
        task.status = status

        for assignee in assignees:
            task.assigned_to.add(User.objects.get(username=assignee))

        task.save()

        return redirect('accounts:home')

    return redirect('accounts:home')

@csrf_exempt
@login_required(login_url='accounts:login')
def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        messages.error(request, "Task doesn't exist")
        return redirect('accounts:home')

    if task:
        if request.user == task.created_by:
            task.delete()
        else:
            messages.error(request, "Only task creator can delete task.")
    else:
        messages.error(request, "Task doesn't exist")

    return redirect('accounts:home')

@csrf_exempt
@login_required()
def post_comment(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        messages.error(request, "Task doesn't exist")
        return redirect('accounts:home')

    if request.method == 'POST':
        body = request.POST.get("comment")
        team_id = request.POST.get("team_id", None)

        flag = False

        if team_id is None:
            if request.user == task.created_by or request.user in task.assigned_to.all():
                flag = True
            else:
                messages.error(request, "You can't comment on this task")
        else:
            team = Team.objects.get(pk=team_id)
            if request.user in team.members.all():
                flag = True
            else:
                messages.error(request, "Only team members can comment on this task")

        if flag:
            comment = Comment(body=body, author=request.user, task=task)

            comment_file = request.FILES.get('comment_file')
            if comment_file:
                fs = FileSystemStorage()
                filename = fs.save(comment_file.name, comment_file)
                comment.file = filename

            comment.save()

    return redirect('tasks:detail', task_id=task_id)

@csrf_exempt
def download_comment_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'comment_files', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        return HttpResponse("File not found", status=404)

@csrf_exempt
def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        return HttpResponse("File not found", status=404)
