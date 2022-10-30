from django.shortcuts import render, get_object_or_404,HttpResponse
from Account.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.

def send_notification(request,user_id):
    user = get_object_or_404(User,pk=user_id)

    title= request.GET.get('title')
    content = request.GET.get('content')

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)({
        f'user_{user.id}_notification',
        {
            'type':'user.notify',
            'notification': {
                'title': title,
                'content': content,
            }
        }
    })

    return HttpResponse(f'notification sent to {user.username}')


