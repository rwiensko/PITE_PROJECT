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
    if ([37, 38, 39, 40].indexOf(event.keyCode) > -1)
     event.preventDefault();
  };
  //The `upHandler`
  key.upHandler = function(event) {
    if (event.keyCode === key.code) {
      if (key.isDown && key.release) key.release();
      key.isDown = false;
      key.isUp = true;
    }
    if ([37, 38, 39, 40].indexOf(event.keyCode) > -1)
     event.preventDefault();
  };
  //Attach event listeners
  window.addEventListener(
    "keydown", key.downHandler, false
  );
  window.addEventListener(
    "keyup", key.upHandler, false
  );
  return key;
}
