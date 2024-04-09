from pyartistry import *

noiseSeed(55)

createCanvas(400, 400)
strokeWeight(5)
stroke(0, 0, 0)

CENTER_X, CENTER_Y = 200, 200
RADIUS = 200

c1 = color(150, 35, 200)
c2 = color(245, 215, 55)

c3 = color(105, 210, 230)
c4 = color(145, 250, 140)

c3 = color(105, 210, 230)
c4 = color(145, 250, 140)

c5 = color(255, 105, 180)

background(c2)
noFill()
stroke(0, 0, 0)
ellipseMode(CENTER)
circle(CENTER_X, CENTER_Y, RADIUS * 2)
circle(CENTER_X / 2, CENTER_Y / 2, RADIUS)
circle(400 - CENTER_X / 4, 400 - CENTER_Y / 4, RADIUS / 2)

for x in range(pg.width):
    for y in range(pg.height):
        n1 = noise(x * 0.02, y * 0.01)
        n2 = noise(x * 0.01, y * 0.02)
        if dist(x, y, CENTER_X, CENTER_Y) <= RADIUS - 4:
            stroke(lerpColor(c1, c2, n1))
            point(x, y)

        if dist(x, y, CENTER_X / 2, CENTER_Y / 2) <= RADIUS / 2 - 4:
            stroke(lerpColor(c2, c3, n2))
            point(x, y)

        if dist(x, y, 400 - CENTER_X / 4, 400 - CENTER_Y / 4) <= RADIUS / 4 - 4:
            stroke(lerpColor(lerpColor(c2, c3, n2), c5, n2))
            point(x, y)

push()
noFill()
stroke(0, 0, 0)
triangle(200, 30, 180, 70, 220, 70)

beginShape()
vertex(180, 70)
vertex(220, 70)
vertex(230, 115)
vertex(170, 115)
endShape(close=True)

line(230, 115, 230, 350)
line(190, 115, 190, 350)
line(210, 115, 210, 350)
line(170, 115, 170, 350)

rect(170, 350, 60, 20, 5)

pop()

show()

save("logo.png")
