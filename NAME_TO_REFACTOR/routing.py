from channels.staticfiles import StaticFilesConsumer
from channels import route, include
from chat.routing import chat_routing
from game_board.routing import game_board_routing

channel_routing = [
    # This makes Django serve static files from settings.STATIC_URL, similar
    # to django.views.static.serve. This isn't ideal (not exactly production
    # quality) but it works for a minimal example.
    route('http.request', StaticFilesConsumer()),
    include(chat_routing, path=r"^/chat"),
    include(game_board_routing, path=r"^/game-board"),
]
