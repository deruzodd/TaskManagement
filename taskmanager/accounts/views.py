from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from tasks.models import Task

from .models import Team

from .forms import CustomUserCreationForm

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register_view(request):
    # Check if user is authenticated, if yes then send to home
    if request.user.is_authenticated:
        return redirect('accounts:home')

    # Handle post request
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Теперь сохраняем пользователя с email

            login(request, user)
            return redirect('accounts:home')
    else:
        # Handle registration route
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


@csrf_exempt
def login_view(request):
    # Check if user is authenticated, if yes then send to home
    if request.user.is_authenticated:
        return redirect('accounts:home')

    # Handle post request
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            ''' Redirect based on next param '''
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            return redirect('accounts:home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@csrf_exempt
@login_required(login_url='accounts:login')
def home_view(request):
    # Get teams of user
    teams = request.user.team_set.all()

    # Get tasks assigned / created to user
    tasks = Task.objects.filter(
        Q(created_by=request.user) | Q(assigned_to=request.user) | Q(team__in=teams)).order_by('title').distinct()

    return render(request, 'home.html', {'tasks': tasks, 'teams': teams})

@csrf_exempt
@login_required()
def create_team(request):
    if request.method == "POST":
        members_list = request.POST.getlist("members")
        team_name = request.POST.get("team_name")

        team = Team.objects.create(
            team_name=team_name, created_by=request.user)

        for member in members_list:
            team.members.add(User.objects.get(username=member))

        # Add creator to members
        team.members.add(request.user)

        team.save()

        # print(members)
        return redirect('accounts:home')

    users = User.objects.all().exclude(username=request.user.username)

    return render(request, 'create_team.html', {'users': users})

@csrf_exempt
@login_required(login_url='accounts:login')
def team_detail(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
    except Team.DoesNotExist:
        messages.error(request, "Team doesn't exist")
        return redirect('accounts:home')

    if request.user not in team.members.all():
        messages.error(
            request, "You are not allowed to view this team's details.")
        return redirect('accounts:home')

    users = User.objects.all()

    tasks = Task.objects.filter(team=team)

    return render(request, 'team_detail.html', {'team': team, 'users': users, 'tasks': tasks})

@csrf_exempt
@login_required()
def add_team_member(request):
    if request.method == 'POST':
        team_id = request.POST.get('team_id', None)

        if team_id is not None:
            try:
                team = Team.objects.get(pk=team_id)
            except Team.DoesNotExist:
                return redirect('accounts:home')
        else:
            return redirect('accounts:home')

        members = request.POST.getlist('members', None)

        if members is not None:
            for member in members:
                team.members.add(User.objects.get(username=member))

    return redirect('accounts:team_detail',
                    team_id=request.POST.get('team_id'))
