from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "tasks"

urlpatterns = [
    path('create/', views.create_task, name='create'),
    path('<int:task_id>/', views.detail, name='detail'),
    path('edit/', views.edit, name='edit'),
    path('delete/<int:task_id>/', views.delete, name='delete'),
    path('comment/<int:task_id>', views.post_comment, name='comment'),
    path('task_files/<path:filename>/', views.download_file, name='download_file'),
    path('comment/<int:task_id>/', views.post_comment, name='comment'),
    path('comment_files/<path:filename>/', views.download_comment_file, name='download_comment_file'),  # Новый URL-шаблон
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)