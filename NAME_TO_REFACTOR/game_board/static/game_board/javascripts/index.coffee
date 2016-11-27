$(document).ready ->
  c = $("#board").get(0)
  ctx = c.getContext("2d")
  ctx.beginPath()
  ctx.arc(200, 200, 100, 0, 2 * Math.PI)
  ctx.fillStyle = "#FF0000"
  ctx.fill()


