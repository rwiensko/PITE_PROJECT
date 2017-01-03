import logging
import json
from channels.sessions import channel_session
from channels import Group

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    log.debug("ws_connect")
    _, player_id = message['path'].decode('ascii').strip('/').split('/')
    data = {'action': 'addPlayer', 'addPlayer': {'id': player_id}}
    Group("game-board").send({"text": json.dumps(data)})
    Group("game-board").add(message.reply_channel)


@channel_session
def ws_receive(message):
    # log.debug("ws_receive")
    data = json.loads(message['text'])
    Group("game-board").send({'text': json.dumps({'action': 'movePlayer', 'movePlayer': data})})

@channel_session
def ws_disconnect(message):
    log.debug("ws_disconnect")
    data = json.loads(message['text'])
    data = {'action': 'removePlayer', 'removePlayer': {'id': 2}}
    Group("game-board").discard(message.reply_channel)
    Group("game-board").send({'text': json.dumps(data)})
