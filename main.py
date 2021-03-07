import pyxel
import enum
import time
import random


class Direction(enum.Enum):
    RIGHT = 0
    LEFT = 1
    DOWN = 2
    UP = 3


class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h)

    def intersects(self, u, v, w, h):
        is_intersected = False
        if (
                u + w > self.x and
                self.x + self.w > u and
                v + h > self.y and
                self.y + self.h > v
        ):
            is_intersected = True
        return is_intersected


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h)



class App:
    def __init__(self):
        self.gameSizeX = 256
        self.gameSizeY = 120
        self.nOfAllWalls = 0
        self.nOfWalls = 40
        pyxel.init(self.gameSizeX, self.gameSizeY, scale=5, caption="NIBBLES", fps=60)
        pyxel.load("assets/resources.pyres.pyxres")
        self.walls = []
        self.initlializeWalls()
        self.player = Player(32, 32)
        self.timeLastFrame = time.time()
        self.dt = 0
        self.timeSinceLastMove = 0
        pyxel.run(self.update, self.draw)

    def update(self):

        self.movePlayer()

        timeThisFrame = time.time()
        self.dt = timeThisFrame - self.timeLastFrame
        self.timeLastFrame = timeThisFrame
        self.timeSinceLastMove += self.dt
        if self.timeSinceLastMove >= 1:
            self.timeSinceLastMove = 0

    def draw(self):
        pyxel.cls(0)
        self.drawWalls()
        self.player.draw()

    def movePlayer(self):
        if not self.checkCollision():
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.player.y += self.player.h
            elif pyxel.btnp(pyxel.KEY_UP):
                self.player.y -= self.player.h
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.player.x -= self.player.w
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.player.x += self.player.w
        if pyxel.btnp(pyxel.KEY_SPACE):
            print()

    def initlializeWalls(self):
        for i in range(self.nOfWalls):
            Xrand = int(random.randrange(1, (self.gameSizeX / 8) - 1))
            Yrand = int(random.randrange(1, (self.gameSizeY / 8) - 1))
            self.walls.append(Wall(Xrand * 8, Yrand * 8))

        for i in range(int(self.gameSizeX / 8)):
            self.walls.append(Wall(i * 8, 0))
            self.walls.append(Wall(i * 8, self.gameSizeY - 8))

        for i in range(int(self.gameSizeY / 8)):
            self.walls.append(Wall(0, i * 8))
            self.walls.append(Wall(self.gameSizeX - 8, i * 8))

    def drawWalls(self):
        self.nOfAllWalls = self.nOfWalls + 2 * int(self.gameSizeX / 8) + 2 * int(self.gameSizeY / 8)
        for i in range(self.nOfAllWalls):
            self.walls[i].draw()

    def checkCollision(self):
        x = self.player.x
        y = self.player.y

        collision = False
        if pyxel.btnp(pyxel.KEY_DOWN):
            y += self.player.h
        elif pyxel.btnp(pyxel.KEY_UP):
            y -= self.player.h
        elif pyxel.btnp(pyxel.KEY_LEFT):
            x -= self.player.w
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            x += self.player.w

        for i in range(self.nOfAllWalls):
            if (
                    self.walls[i].x == x and
                    self.walls[i].y == y
            ):
                collision = True
        return collision


App()
