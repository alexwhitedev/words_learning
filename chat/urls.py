from django.urls import path

from . import views
from chat.models import ConnectedUsers

urlpatterns = [
    path('webhook/', views.webhook),
    path('online/', views.UsersOnline.as_view(), name='online'),
    path('', views.index, name='index'),
    path('/chatroom/<str:room_name>/', views.room, name='room'),
    path('run_tasks/', views.run_task),
    path('send_email_task/', views.send_email_task),
]

ConnectedUsers.objects.all().delete()
