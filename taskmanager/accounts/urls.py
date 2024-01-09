from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('home/', views.home_view, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('create_team/', views.create_team, name="create_team"),
    path('team/<int:team_id>/', views.team_detail, name="team_detail"),
    path('team/add_member/', views.add_team_member, name="add_team_member"),


]

#     path('password_reset/', views.custom_password_reset_view, name='password_reset'),
#     path('password_reset/done/', views.custom_password_reset_done_view, name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm_view, name='password_reset_confirm'),
#     path('reset/done/', views.custom_password_reset_complete_view, name='password_reset_complete'),
# ]