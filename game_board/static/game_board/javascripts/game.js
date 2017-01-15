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

    var gameStage = new Container();
    var stage = new Container();
    var gameOverStage = new Container();

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

            if (j == 5 && i%5==1){
                var diamond = PIXI.Sprite.fromImage("/static/game_board/images/diamond.png");
                diamond.buttonMode = true;
                diamond.x = 40*i;
                diamond.y = 40*j;
                diamond.interactive = true;
                diamond.on('mousedown', setHaveDiamondToTrue);
                stage.addChild(diamond);
            }
            if (j<9){
                if (i%5 == 1 && j==5) continue
                var brick = PIXI.Sprite.fromImage("/static/game_board/images/brick.png");
                brick.buttonMode = true;
                brick.x = 40*i;
                brick.y = 40*j;
                brick.interactive = true;
                brick.on('mousedown', sendRequestToRemoveBrick);
                stage.addChild(brick);
            }
            if (j>8 && j<14){
                var rock_brick = PIXI.Sprite.fromImage("/static/game_board/images/rock_brick.png");
                rock_brick.buttonMode = true;
                rock_brick.x = 40*i;
                rock_brick.y = 40*j;
                rock_brick.interactive = true;
                rock_brick.on('mousedown', sendRequestToRemoveRockBrick);
                stage.addChild(rock_brick);
            }
            if (j == 14){
                var gold = PIXI.Sprite.fromImage("/static/game_board/images/gold_brick.png");
                gold.buttonMode = true;
                gold.x = 40*i;
                gold.y = 40*j;
                gold.interactive = true;
                gold.on('mousedown', sendRequestPlayerWon);
                stage.addChild(gold);
            }

        };
    };

    function sendRequestPlayerWon(){
        var id =stage.getChildIndex(this);
        console.log("gold id: " +id)
        var message = {
            action: 'remove_gold',
            remove_gold: {
            id: id,
            }
        };

    if ( Math.abs(this.x - player.x) <80 && Math.abs(this.y - player.y)  <80 ){
        chatsock.send(JSON.stringify(message));
      }
    }

    function gameOver(data){
        var gold = PIXI.Sprite.fromImage("/static/game_board/images/gold_brick.png");
        gold.x = 40;
        gold.y = 40;
        gameOverStage.addChild(gold);
        var endText = new PIXI.Text('Player: ', { font: 'bold italic 60px Arvo', fill: '#3e1707', align: 'center', stroke: '#a4410e', strokeThickness: 7 });
        endText.text = 'Player: ' + data['username'] + ' won';
        endText.position.x = 100;
        endText.position.y = 100;
        gameOverStage.addChild(endText);
        stage.visible = false;
        gameOverStage.visible = true;
    }

    function setHaveDiamondToTrue(){
        var id =stage.getChildIndex(this);
        console.log("diamond id: " +id)
        var message = {
            action: 'remove_diamond',
            remove_diamond: {
            id: id,
            }
        };

    if ( Math.abs(this.x - player.x) <80 && Math.abs(this.y - player.y)  <80 ){
        player.have_diamond = true;
        chatsock.send(JSON.stringify(message));
      }
    }

    function sendRequestToRemoveRockBrick(){
        var id =stage.getChildIndex(this);
        console.log("remove rock brick: " +id)
        var message = {
            action: 'remove_rock_brick',
            remove_rock_brick: {
            id: id,
            }
        };

    if ( Math.abs(this.x - player.x) <80 && Math.abs(this.y - player.y)  <80  && player.have_diamond == true){
        chatsock.send(JSON.stringify(message));
      }

    }

    function sendRequestToRemoveBrick(){
      var id = stage.getChildIndex(this);
      console.log("remove brick heh: " + id);
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
        console.log("remove brick: " + data.id);
        stage.removeChildAt(data.id);
    }


    function setup() {
      player = new Sprite(
        loader.resources["/static/game_board/images/avatar.png"].texture
      );
      player.scale.set(0.35, 0.35);
      player.x = 10;
      player.y = 10;
      player.field = {x: 0, y: 0};
      player.vx = 0;
      player.vy = 0;
      player.id = player_id;
      player.have_diamond = false;
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
          player.field["x"] -= 1;
        };

        up.press = function() {
          player.field["y"] -= 1;
        };

        right.press = function() {
          player.field["x"] += 1;
        };

        down.press = function() {
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
      if (last_x != player.x || last_y != player.y)
        chatsock.send(JSON.stringify(message));


      last_x = player.x;
      last_y = player.y;
      counter += 1;
      gameStage.addChild(stage);
      gameStage.addChild(gameOverStage);
      renderer.render(gameStage);
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
        removeBrick(data.remove_brick);
        break;
       case "remove_rock_brick":
        removeBrick(data.remove_rock_brick);
        break;
       case "remove_diamond":
        removeBrick(data.remove_diamond);
        break;
       case "remove_gold":
        gameOver(data.remove_gold);
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
});
