from tkinter import mainloop, BOTH, Canvas, Tk
from random import randrange as rnd, choice
import math

root = Tk()
root.geometry('1280x720')
c = Canvas(root, bg='white')
c.pack(fill=BOTH, expand=1)
colors = ['red', 'pink']  # Color module


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, v):
        self.x += v.x
        self.y += v.y
        return self

    def __mul__(self, c):
        return Vector(self.x * c, self.y * c)

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def multiply(self, c):
        self.x = c * self.x
        self.y = c * self.y


class Ball:  # Class ball, move, acceleration, reflection are included. POS-X and Y-needs to seek POSition of the >
    # < ball and make some math.
    # VEL - VELocity, X and Y components are included, needs to seek VELocity and track the ball
    # ACC - ACCeleration, X and Y components are included, needs for collisions with ONLY WALLS(!)
    # RF - acceleration, X and Y components are included, need for ONLY BALL-BALL COLLISIONS(!)
    # R - Radius, needs to create ball, and for math
    # T - internal variable, need to BALL-BALL COLLISION math
    # OBJ - object that you see, made of POS and R, color is random
    # AIRRES - AIRRESistance, needs to limit velocity
    # G - gravity
    def __init__(self):
        self.pos = Vector(rnd(100, 1200), rnd(100, 600))
        self.vel = Vector(rnd(-10, 10), rnd(-10, 10))
        self.acc = Vector(0, 0)
        self.rf = Vector(0, 0)
        self.airres = Vector(0, 0)
        self.g = Vector(0, 0.5)
        self.r = 25
        self.t = 0
        self.obj = c.create_oval(self.pos.x - self.r, self.pos.y - self.r, self.pos.x + self.r,
                                 self.pos.y + self.r,
                                 fill=choice(colors), width=0)

    def move(self):  # Move with acceleration, works
        self.vel += self.acc
        self.vel += self.rf
        self.vel += self.airres
        self.vel += self.g
        self.pos += self.vel
        c.move(self.obj, self.vel.x, self.vel.y)

    def reflection(self):  # Wall collision, uses acceleration, not impulses, works
        if self.pos.x < self.r:
            self.acc.x = self.r - self.pos.x
        elif self.pos.x > 1280 - self.r:
            self.acc.x = 1280 - self.pos.x - self.r
        else:
            self.acc.x = 0
        if self.pos.y < self.r:
            self.acc.y = self.r - self.pos.y
        elif self.pos.y > 720 - self.r:
            self.acc.y = 720 - self.pos.y - self.r
        else:
            self.acc.y = 0

    def collision(self, ball):  # collision module, uses acceleration, affect to 1st and 2nd ball(!), works
        if ((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2) < (self.r + ball.r):
            r = self.r + ball.r - (((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2))
            sin = math.fabs((self.pos.x - ball.pos.x) / (
                    ((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2)))
            cos = math.fabs((self.pos.y - ball.pos.y) / (
                    ((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2)))
            if self.pos.x > ball.pos.x:
                self.rf.x = r * sin
                ball.rf.x = - r * sin
            else:
                self.rf.x = - r * sin
                ball.rf.x = r * sin
            if self.pos.y > ball.pos.y:
                self.rf.y = r * cos
                ball.rf.y = - r * cos
            else:
                self.rf.y = - r * cos
                ball.rf.y = r * cos

    def check(self, ball):  # add function, check if balls collide, add t +=1
        if ((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2) < (self.r + ball.r):
            self.t += 1

    def zerorf(self):  # add function, resets Racceleration to zero if t = 0 (noone ball are near this ball)
        if self.t == 0:
            self.rf.x = 0
            self.rf.y = 0

    def airresistance(self, k):  # airresistance mosule, limits velocity
        if math.fabs(self.vel.x) > 5:
            self.airres.x = -1 * k * (self.vel.x) * math.fabs(self.vel.x)
        if math.fabs(self.vel.y) > 5:
            self.airres.y = -1 * k * (self.vel.y) * math.fabs(self.vel.y)


def rfdelete(list):  # check function, needs to seek Racceleration cause it complicated, uses *zerorf and *check(!)
    for i in range(len(list)):
        for g in range(len(list)):
            if i != g:
                list[g].check(list[i])
    for k in range(len(list)):
        list[k].zerorf()


def cleart(list):  # add function, needs to clear t after collisions
    for i in range(len(list)):
        list[i].t = 0


def mover(list):  # add fuction, includes move() of the ALL balls in the list
    for i in range(len(list)):
        list[i].move()


def reflector(list):  # add function, includes reflection() of the ALL balls in the list
    for i in range(len(list)):
        list[i].reflection()


def air(list, k):  # add function, includes airresistance() of the ALL balls in the list
    for i in range(len(list)):
        list[i].airresistance(k)


def collider(list):  # add function, includes collision() of the ALL ball-ball in the list
    for i in range(len(list)):
        for g in range(len(list)):
            if i != g:
                list[g].collision(list[i])


ballpack = [Ball() for i in range(10)]


def update():  # Time function
    reflector(ballpack)
    air(ballpack, 0.0003)
    collider(ballpack)
    rfdelete(ballpack)
    mover(ballpack)
    cleart(ballpack)

    root.after(10, update)


update()
mainloop()