from django.shortcuts import render
from game_board.models import Player
# Create your views here.

def index(request):
    player = Player.objects.create()
    return render(request, 'game_board/index.html', {
        'player': player
    })
