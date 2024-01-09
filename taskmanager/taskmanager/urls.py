from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('tasks/', include('tasks.urls'))
]
