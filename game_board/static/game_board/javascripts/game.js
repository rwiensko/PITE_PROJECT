$(function() {
    // Websockets
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var player_id = $('#main-content').data('player-id');
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname + player_id + '/');

    window.onbeforeunload = function(e) {
      chatsock.send(JSON.stringify({action: "remove_player", remove_player: {id: player_id}}));
    }

    // Aliases
    var autoDetectRenderer = PIXI.autoDetectRenderer;
    var Container = PIXI.Container;
    var loader = PIXI.loader;
    var Sprite = PIXI.Sprite;

    var stage = new Container();
    var renderer = autoDetectRenderer(800, 600,{backgroundColor : 0x1099bb});
    $(renderer.view).appendTo("#main-content");

    loader
      .add("/static/game_board/images/avatar.png")
      .add("/static/game_board/images/brick.png")
      .load(setup);

    var player ;
    var players = {};
    var counter = 0;
    //set stage
    var fields = [];

    function removeHeh(){
        stage.removeChild(this);
    }

    function sendRequestToRemoveBrick(){
      var id = stage.getChildIndex(this)
      console.log("remove brick heh: " + id);
      //stage.removeChild(this);
      var message = {
        action: 'remove_brick',
        remove_brick: {
          id: id,
          field: this.field
        }
      };

      if ( Math.abs(this.x - player.x) <80 && Math.abs(this.y - player.y) <80){
        chatsock.send(JSON.stringify(message));
      }
    }

    function removeBrick(data){
        var sprite = stage.get
        fields[data.field["y"]][data.field["x"]] = false;
        stage.removeChildAt(data.id);
    }


    function setup() {

      // Setup fields
      for(var j = 0; j < 15; j++){
        fields[j] = [];
        for(var i = 0; i < 20; i++)
          fields[j][i] = j > 1;
      }

      // draw bricks
      for (var j = 2; j < 15; j++) {
        for (var i = 0; i < 20; i++) {
          drawBrick(i, j);
        };
      };

      player = new Sprite(
        loader.resources["/static/game_board/images/avatar.png"].texture
      );
      player.scale.set(0.35, 0.35);
      player.x = 10;
      player.y = 10;
      player.last_x = player.x;
      player.last_y = player.y;
      player.field = {x: 0, y: 0};
      player.id = player_id;
      stage.addChild(player);

      var players_ids = $('#main-content').data('players-ids');
      for(var i in players_ids){
        addPlayer(players_ids[i]);
      }

      var left = keyboard(37),
        up = keyboard(38),
        right = keyboard(39),
        down = keyboard(40);

        left.press = function() {
          var field = {
            x: player.field["x"] - 1,
            y: player.field["y"]
          };
          if(canMoveTo(field["x"], field["y"]))
            player.field["x"] -= 1;
        };

        up.press = function() {
          var field = {
            x: player.field["x"],
            y: player.field["y"] - 1
          };
          if(canMoveTo(field["x"], field["y"]))
            player.field["y"] -= 1;
        };

        right.press = function() {
          var field = {
            x: player.field["x"] + 1,
            y: player.field["y"]
          };
          if(canMoveTo(field["x"], field["y"]))
            player.field["x"] += 1;
        };

        down.press = function() {
          var field = {
            x: player.field["x"],
            y: player.field["y"] + 1
          };
          if(canMoveTo(field["x"], field["y"]))
            player.field["y"] += 1;
        };

      chatsock.onmessage = websocketListener;
      chatsock.onclose = closeWebsocketHandler;
      gameLoop();
    }

    function gameLoop() {
      requestAnimationFrame(gameLoop);

      player.x = player.field["x"] * 40;
      player.y = player.field["y"] * 40;
      var message = {
        action: 'move_player',
        move_player: {
          id: player.id,
          x: player.x,
          y: player.y
        }
      };
      if (player.last_x != player.x || player.last_y != player.y)
        chatsock.send(JSON.stringify(message));


      player.last_x = player.x;
      player.last_y = player.y;
      counter += 1;

      renderer.render(stage);
    }

  function websocketListener(message) {
    var data = JSON.parse(message.data);
    switch (data.action) {
      case "add_player":
        addPlayer(data.add_player);
        break;
      case "remove_player":
        removePlayer(data.remove_player);
        break;
      case "move_player":
        movePlayer(data.move_player);
        break;
       case "remove_brick":
        removeBrick(data.remove_brick); //dodaj message do SendRequestToDeleteBrick
        break;
      default:
        console.log(data);
    }
  }

  function closeWebsocketHandler(event) {

    for(var id in players){
      players[id].destroy();
      console.log(id);
    }
  }

  function addPlayer(data) {
    console.log("add player with id: " + data.id);
    var id = data.id;
    players[id] = new Sprite(
      loader.resources["/static/game_board/images/avatar.png"].texture
    );
    console.log(players);

    var new_player = players[id];

    new_player.scale.set(0.3125, 0.3125);
    new_player.x = 10;
    new_player.y = 10;
    stage.addChild(new_player);
  }

  function removePlayer(data) {
    var id = data.id;
    players[id].destroy();
  }

  function movePlayer(data) {
    console.log("move player with id: " + data.id);
    if (data.id != player_id) {
      var moved_player = players[data.id];
      moved_player.x = data.x;
      moved_player.y = data.y;
    }
  }

  function canMoveTo(i, j) {
    var in_bounds = i >= 0 && j >= 0 && i < 20 && j < 15;
    return in_bounds && !fields[j][i];
  }

  function drawBrick(i, j) {
    var brick = new Sprite(
      loader.resources["/static/game_board/images/brick.png"].texture
    );
    brick.buttonMode = true;
    brick.x = 40*i;
    brick.y = 40*j;
    brick.field = {x: i, y: j};
    brick.interactive = true;
    brick.on('mousedown', sendRequestToRemoveBrick);
    stage.addChild(brick);
  }
});
