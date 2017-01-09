import logging
import json
from channels.sessions import channel_session
from channels import Group
from chat.models import Room
from game_board.models import Player

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    log.debug("ws_connect")
    _, label, player_id = message['path'].decode('ascii').strip('/').split('/')
    room = Room.objects.get(label=label)
    data = {'action': 'add_player', 'add_player': {'id': player_id}}
    Group("game-board-" + label).send({"text": json.dumps(data)})
    Group("game-board-" + label).add(message.reply_channel)

    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    data = json.loads(message['text'])
    label = message.channel_session['room']
    log.debug(data['action'])
    if data['action'] == 'remove_player':
        Player.objects.filter(id=data['remove_player']['id']).delete()
    Group("game-board-" + label).send({'text': json.dumps(data)})

@channel_session
def ws_disconnect(message):
    log.debug("ws_disconnect")
    data = {'action': 'remove_player', 'remove_player': {'id': 2}}
    label = message.channel_session['room']
    Group("game-board-" + label).discard(message.reply_channel)
    Group("game-board-" + label).send({'text': json.dumps(data)})
