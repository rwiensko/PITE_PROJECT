import logging
import json
from channels.sessions import channel_session
from channels import Group
from game_board.models import Player

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    log.debug("ws_connect")
    _, player_id = message['path'].decode('ascii').strip('/').split('/')
    data = {'action': 'add_player', 'add_player': {'id': player_id}}
    Group("game-board").send({"text": json.dumps(data)})
    Group("game-board").add(message.reply_channel)


@channel_session
def ws_receive(message):
    data = json.loads(message['text'])
    log.debug(data['action'])
    if data['action'] == 'remove_player':
        Player.objects.filter(id=data['remove_player']['id']).delete()
    if data['action'] == 'remove_brick':
        Group("game-board").send({'text' : json.dumps(data)})



@channel_session
def ws_disconnect(message):
    log.debug("ws_disconnect")
    data = {'action': 'remove_player', 'remove_player': {'id': 2}}
    Group("game-board").discard(message.reply_channel)
    Group("game-board").send({'text': json.dumps(data)})
