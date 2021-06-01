from django.urls import path

from . import views

urlpatterns = [
    path('webhook/', views.webhook),
    path('online/', views.UsersOnline.as_view(), name='online'),
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]

from chat.models import ConnectedUsers

ConnectedUsers.objects.all().delete()
