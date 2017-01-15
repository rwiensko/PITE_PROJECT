import json
from channels import Group
from channels.sessions import channel_session
from chat.models import Room


@channel_session
def ws_connect(message):
    _, label = message['path'].decode('ascii').strip('/').split('/')
    room = Room.objects.get(label=label)
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session['room'] = room.label

@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    room = Room.objects.get(label=label)
    data = json.loads(message['text'])
    m = room.messages.create(**data)
    Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    room = Room.objects.get(label=label)
    Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
