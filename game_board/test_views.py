from django.test import TestCase
from chat.models import Room, Message
from game_board.models import Player
from django.contrib.auth.models import User
import json

class ViewTests(TestCase):
    def setUp(self):
        current_user = User.objects.create_user("wojtek", "wojtarz@tlen.pl", "marik1234")
        current_user.is_active = True
        self.client.login(username="wojtek", password="marik1234")

    def test_index(self):
        r = self.client.get('/game-board/')
        self.assertTemplateUsed(r, 'game_board/index.html')

    def test_new_room(self):
        r = self.client.get('/game-board/new/')
        _, room_label = r['Location'].strip('/').split('/')
        assert Room.objects.filter(label=room_label).exists()
        self.assertRedirects(r, '/game-board/' + room_label + '/')

    def test_game_room(self):
        room = Room.objects.create(label='room1')
        r = self.client.get('/game-board/room1/')
        player = Player.objects.last()
        self.assertTemplateUsed(r, 'game_board/room.html')
        self.assertEqual(r.context['player'], player)
        self.assertEqual(r.context['room'], room)
        self.assertEqual('room1', player.label)

        another_response = self.client.get('/game-board/room1/')
        players_ids = json.loads(another_response.context['players_ids'])
        self.assertEqual([{u'id': player.id}], players_ids)
