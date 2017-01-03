from django.shortcuts import render
from game_board.models import Player
import json
# Create your views here.

def index(request):
    players_ids = list(Player.objects.values('id'))
    players_ids = json.dumps(players_ids)
    player = Player.objects.create()

    return render(request, 'game_board/index.html', {
        'player': player,
        'players_ids': players_ids
    })
