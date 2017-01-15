from channels import Channel, Group
from channels.tests import ChannelTestCase
from chat.consumers import ws_connect, ws_receive, ws_disconnect
from chat.models import Room
import json

class TestConsumers(ChannelTestCase):
    def setUp(self):
        self.room = Room.objects.create(label="dodoni")

    def test_ws_connect(self):
        Channel(u"my-channel").send({})
        message = self.get_next_message(u"my-channel", require=True)
        message['path'] = "/chat/dodoni/"
        message.reply_channel = Channel(u"reply-channel")
        ws_connect(message)
        self.assertIsNone(self.get_next_message(u"my-channel", require=False))
        self.assertEqual(message.channel_session['room'], "dodoni")
        assert 'reply-channel' in message.channel_layer._groups[u"chat-dodoni"]

    def test_ws_receive(self):
        Group(u"chat-dodoni").add(u"my-channel")
        Group(u"chat-dodoni").send({
            "text": json.dumps({
                "handle": "RaV",
                "message": "Kalambury jestem bury"
            })
        })
        message = self.get_next_message(u"my-channel", require=True)
        message['path'] = "/chat/dodoni/"
        message.reply_channel = Channel(u"reply-channel")
        ws_connect(message)
        ws_receive(message)
        result = self.get_next_message(u"my-channel", require=True)
        data = json.loads(result['text'])
        self.assertEqual(data['handle'], "RaV")
        self.assertEqual(data['message'], "Kalambury jestem bury")

    def test_ws_disconnect(self):
        Group(u"chat-dodoni").add(u"my-channel")
        Channel(u"my-channel").send({})
        message = self.get_next_message(u"my-channel", require=True)
        message['path'] = "/chat/dodoni/"
        message.reply_channel = Channel(u"reply-channel")
        ws_connect(message)
        ws_disconnect(message)
        assert 'reply-channel' not in message.channel_layer._groups[u"chat-dodoni"]
