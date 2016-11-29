$(document).ready ->
  drawBall("#FF0000")
  printUserName()
  clicked = false

  $("#board").click ->
    clicked = !clicked
    clearCanvas()
    color = if clicked then "#0000FF" else "#FF0000"
    drawBall(color)
    printUserName()


drawBall = (color)->
  canvas = $("#board").get(0)
  ctx = canvas.getContext("2d")
  ctx.beginPath()
  ctx.arc(200, 200, 100, 0, 2 * Math.PI)
  ctx.fillStyle = color
  ctx.fill()

printUserName = ->
  userName = $("#main-content").data("username") || "guest"
  canvas = $("#board").get(0)
  ctx = canvas.getContext("2d")
  ctx.font = "30px Arial"
  ctx.fillStyle = "#FFFFFF"
  ctx.fillText(userName, 150, 200)

clearCanvas = ->
  canvas = $("#board").get(0)
  ctx = canvas.getContext("2d")
  ctx.clearRect(0, 0, canvas.width, canvas.height)
