from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from haikunator import Haikunator
from chat.models import Room
from game_board.models import Player
import json
# Create your views here.

def index(request):
    return render(request, 'game_board/index.html')

@login_required
def new_room(request):
    new_room = None
    haikunator = Haikunator()
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect('game_board:game_room', label=label)

@login_required
def game_room(request, label):
    players_ids = list(Player.objects.filter(label=label).values('id'))
    players_ids = json.dumps(players_ids)
    player = Player.objects.create(label=label)
    room, created = Room.objects.get_or_create(label=label)
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "game_board/room.html", {
        'player': player,
        'players_ids': players_ids,
        'room': room,
        'messages': messages,
    })
