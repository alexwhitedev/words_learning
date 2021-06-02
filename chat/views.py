from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from chat.models import ConnectedUsers
from chat.tasks import add, mul, shared_task, send_email
from datetime import datetime

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


def run_task(request):
    sum_task_id = add.delay(2, 5)
    ml_task_id = mul.delay(2, 5)

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    return HttpResponse('Task1 name: \"%s\", job: \"%s\" res: %s time: %s ------ \nTask2 name: \"%s\" job: \"%s\" res: %s time: %s'
                        % (add.name, sum_task_id, sum_task_id.get(), current_time, mul.name, ml_task_id, ml_task_id.get(), current_time))


def send_email_task(request):
    email_task_id = send_email.delay(['wordslearning.notificator@gmail.com'],)
    return HttpResponse(f'The jobs for sending email in progress. Wait for finish. Task id {email_task_id}')
