from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from chat.models import ConnectedUsers

import datetime


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def webhook(request):
    channel_layer = get_channel_layer()
    if not channel_layer.groups:
        return HttpResponse('No any groups available')
    async_to_sync(channel_layer.group_send)(
        list(channel_layer.groups.keys())[0],
        {
            'type': 'chat_message',
            'message': 'Hello from the Web. Current time is %s' % datetime.datetime.now()
        }
    )
    return HttpResponse("Result is OK. Check windows of the firstly created chat for a new message")


def users_online(request):
    connected_users = [str(user) for user in ConnectedUsers.objects.all()]
    return HttpResponse("Currently connected: %s" % connected_users)


class UsersOnline(LoginRequiredMixin, ListView):
    model = ConnectedUsers
    context_object_name = 'users'
    template_name = 'chat/online.html'