// Generated by CoffeeScript 1.11.1
(function() {
  var clearCanvas, drawBall, printUserName;

  $(document).ready(function() {
    var clicked;
    drawBall("#FF0000");
    printUserName();
    clicked = false;
    return $("#board").click(function() {
      var color;
      clicked = !clicked;
      clearCanvas();
      color = clicked ? "#0000FF" : "#FF0000";
      drawBall(color);
      return printUserName();
    });
  });

  drawBall = function(color) {
    var canvas, ctx;
    canvas = $("#board").get(0);
    ctx = canvas.getContext("2d");
    ctx.beginPath();
    ctx.arc(200, 200, 100, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    return ctx.fill();
  };

  printUserName = function() {
    var canvas, ctx, userName;
    userName = $("#main-content").data("username") || "guest";
    canvas = $("#board").get(0);
    ctx = canvas.getContext("2d");
    ctx.font = "30px Arial";
    ctx.fillStyle = "#FFFFFF";
    return ctx.fillText(userName, 150, 200);
  };

  clearCanvas = function() {
    var canvas, ctx;
    canvas = $("#board").get(0);
    ctx = canvas.getContext("2d");
    return ctx.clearRect(0, 0, canvas.width, canvas.height);
  };

}).call(this);
