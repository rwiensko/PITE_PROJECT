from django.test import TestCase
from chat.models import Room, Message
from django.contrib.auth.models import User

class ViewTests(TestCase):
    def setUp(self):
        current_user = User.objects.create_user("wojtek", "wojtarz@tlen.pl", "marik1234")
        current_user.is_active = True
        self.client.login(username="wojtek", password="marik1234")

    def test_about(self):
        r = self.client.get('/chat/')
        self.assertTemplateUsed(r, 'chat/about.html')

    def test_new_room(self):
        r = self.client.get('/chat/new/')
        _, room_label = r['Location'].strip('/').split('/')
        assert Room.objects.filter(label=room_label).exists()

    def test_chat_room(self):
        room = Room.objects.create(label='room1')
        r = self.client.get('/chat/room1/')
        self.assertTemplateUsed(r, 'chat/room.html')
        assert r.context['room'] == room
