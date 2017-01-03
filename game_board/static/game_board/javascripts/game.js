$(function() {
    // Websockets
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var player_id = $('#main-content').data('player-id');
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname + player_id + '/');

    window.onbeforeunload = function(e) {

    }

    // Aliases
    var autoDetectRenderer = PIXI.autoDetectRenderer;
    var Container = PIXI.Container;
    var loader = PIXI.loader;
    var Sprite = PIXI.Sprite;

    var stage = new Container();
    var renderer = autoDetectRenderer(400, 400);
    $(renderer.view).appendTo("#main-content");

    loader
      .add("/static/game_board/images/avatar.png")
      .load(setup);

    var player;
    var players = {};
    var last_x = 0, last_y = 0;

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
      gameLoop();
    }

    function gameLoop() {
      requestAnimationFrame(gameLoop);

      player.x += player.vx;
      player.y += player.vy;
      var message = {
        id: player.id,
        x: player.x,
        y: player.y
      };
      if (last_x != player.x || last_y != player.y) {
        chatsock.send(JSON.stringify(message));
      }
      last_x = player.x;
      last_y = player.y;

      renderer.render(stage);
    }

  function websocketListener(message) {
    var data = JSON.parse(message.data);
    switch (data.action) {
      case "addPlayer":
        addPlayer(data.addPlayer);
        break;
      case "removePlayer":
        removePlayer(data.removePlayer);
        break;
      case "movePlayer":
        movePlayer(data.movePlayer);
        break;
      default:
        console.log(data);
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
