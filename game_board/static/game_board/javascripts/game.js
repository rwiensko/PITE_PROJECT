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
      .load(setup);

    var player;
    var players = {};
    var last_x = 0, last_y = 0, counter = 0;
    //set stage

    for (var j = 2; j < 15; j++) {

        for (var i = 0; i < 20; i++) {
            var brick = PIXI.Sprite.fromImage("/static/game_board/images/brick.png");
            brick.buttonMode = true;
            brick.x = 40*i;
            brick.y = 40*j;
            brick.interactive = true;
            brick.on('mousedown', sendRequestToRemoveBrick);
            stage.addChild(brick);
        };
    };

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
        }
      };

      if ( Math.abs(this.x - player.x) <80 && Math.abs(this.y - player.y) <80){
        chatsock.send(JSON.stringify(message));
      }
    }

    function removeBrick(data){
        var sprite = stage.get
        console.log("remove brick: " + data.id);
        stage.removeChildAt(data.id);
    }


    function setup() {
      player = new Sprite(
        loader.resources["/static/game_board/images/avatar.png"].texture
      );
      player.scale.set(0.5, 0.5);
      player.x = 10;
      player.y = 10;
      player.vx = 0;
      player.vy = 0;
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
          player.vx = -5;
          player.vy = 0;
        };
        left.release = function() {
          if (!right.isDown && player.vy === 0) {
          player.vx = 0;
          }
        };

        up.press = function() {
          player.vy = -5;
          player.vx = 0;
        };
        up.release = function() {
          if (!down.isDown && player.vx === 0) {
          player.vy = 0;
          }
        };

        right.press = function() {
          player.vx = 5;
          player.vy = 0;
        };
        right.release = function() {
          if (!left.isDown && player.vy === 0) {
          player.vx = 0;
          }
        };

        down.press = function() {
          player.vy = 5;
          player.vx = 0;
        };
        down.release = function() {
          if (!up.isDown && player.vx === 0) {
          player.vy = 0;
          }
        };

      chatsock.onmessage = websocketListener;
      chatsock.onclose = closeWebsocketHandler;
      gameLoop();
    }

    function gameLoop() {
      requestAnimationFrame(gameLoop);

      player.x += player.vx;
      player.y += player.vy;
      var message = {
        action: 'move_player',
        move_player: {
          id: player.id,
          x: player.x,
          y: player.y
        }
      };
      if (counter %5 == 0 && (last_x != player.x || last_y != player.y)) {
        chatsock.send(JSON.stringify(message));
      }

      last_x = player.x;
      last_y = player.y;
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

    new_player.scale.set(0.5, 0.5);
    new_player.x = 10;
    new_player.y = 10;
    new_player.vx = 0;
    new_player.vy = 0;
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

  function keyboard(keyCode) {
    var key = {};
    key.code = keyCode;
    key.isDown = false;
    key.isUp = true;
    key.press = undefined;
    key.release = undefined;
    //The `downHandler`
    key.downHandler = function(event) {
      if (event.keyCode === key.code) {
        if (key.isUp && key.press) key.press();
        key.isDown = true;
        key.isUp = false;
      }
      event.preventDefault();
    };
    //The `upHandler`
    key.upHandler = function(event) {
      if (event.keyCode === key.code) {
        if (key.isDown && key.release) key.release();
        key.isDown = false;
        key.isUp = true;
      }
      event.preventDefault();
    };
    //Attach event listeners
    window.addEventListener(
      "keydown", key.downHandler.bind(key), false
    );
    window.addEventListener(
      "keyup", key.upHandler.bind(key), false
    );
    return key;
  }
});
