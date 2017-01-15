from channels import Channel, Group
from channels.tests import ChannelTestCase
from django.contrib.auth.models import User
from game_board.consumers import ws_connect, ws_receive, ws_disconnect
from game_board.models import Player
from chat.models import Room
import json

class TestConsumers(ChannelTestCase):
    def setUp(self):
        self.room = Room.objects.create(label="dodoni")
        self.current_user = User.objects.create_user("wojtek", "wojtarz@tlen.pl", "marik1234")
        self.current_user.is_active = True

    def test_ws_connect(self):
        Channel(u"first-channel").send({})
        message = self.get_next_message(u"first-channel", require=True)
        message['path'] = "/game-board/dodoni/1/"
        message.reply_channel = Channel(u"first-reply-channel")
        ws_connect(message)

        Channel(u"second-channel").send({})
        second_message = self.get_next_message(u"second-channel", require=True)
        second_message['path'] = "/game-board/dodoni/2/"
        second_message.reply_channel = Channel(u"second-reply-channel")
        ws_connect(second_message)

        result = self.get_next_message(u"first-reply-channel", require=True)
        data = json.loads(result['text'])
        self.assertEqual(data, {
            u'action': u'add_player',
            u'add_player': {u'id': u'2'}
        })
        self.assertEqual(message.channel_session['room'], "dodoni")
        assert 'first-reply-channel' in message.channel_layer._groups[u"game-board-dodoni"]
        assert 'second-reply-channel' in message.channel_layer._groups[u"game-board-dodoni"]

    def test_ws_receive(self):
        Channel(u"channel").send({
            'text': json.dumps({
                'action': 'remove_player',
                'remove_player': {'id': 1}
            })
        })
        message = self.get_next_message(u"channel", require=True)
        message['path'] = "/game-board/dodoni/1/"
        message.reply_channel = Channel(u"reply-channel")
        player = Player.objects.create(label="dodoni", user=self.current_user)
        ws_connect(message)
        ws_receive(message)
        self.assertEqual(len(Player.objects.filter(id=1)), 0)
        result = self.get_next_message(u"reply-channel", require=True)
        data = json.loads(result['text'])
        self.assertEqual(data, {
            'action': 'remove_player',
            'remove_player': {'id': 1}
        })

    def test_destroy_room(self):
        Channel(u"channel").send({
            'text': json.dumps({
                'action': 'destroy_room',
            })
        })
        message = self.get_next_message(u"channel", require=True)
        message['path'] = "/game-board/dodoni/1"
        message.reply_channel = Channel(u"reply-channel")
        ws_connect(message)
        ws_receive(message)
        self.assertEqual(len(Room.objects.all()), 0)

    def test_ws_disconnect(self):
        Channel(u"first-channel").send({})
        message = self.get_next_message(u"first-channel", require=True)
        message['path'] = "/game-board/dodoni/1/"
        message.reply_channel = Channel(u"first-reply-channel")
        ws_connect(message)

        Channel(u"second-channel").send({})
        second_message = self.get_next_message(u"second-channel", require=True)
        second_message['path'] = "/game-board/dodoni/2/"
        second_message.reply_channel = Channel(u"second-reply-channel")
        ws_connect(second_message)
        ws_disconnect(second_message)

        assert 'second-reply-channel' not in message.channel_layer._groups[u"game-board-dodoni"]
