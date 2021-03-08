import pyxel
import enum
import time
import random


# paste into terminal to enter pyxel editor
# pyxeleditor resources.pyres.pyxres
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

    def moveWall(self, direction):
        if direction == Direction.LEFT:
            self.x -= self.w
        if direction == Direction.RIGHT:
            self.x += self.w
        if direction == Direction.UP:
            self.y -= self.h
        if direction == Direction.DOWN:
            self.y += self.h


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
        self.nOfWalls = 41
        self.nOfSideWalls = 0
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
        a = 0
        if not self.checkCollision(self.player):
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.player.y += self.player.h
            elif pyxel.btnp(pyxel.KEY_UP):
                self.player.y -= self.player.h
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.player.x -= self.player.w
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.player.x += self.player.w
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.walls[self.nOfSideWalls].moveWall(Direction.LEFT)

    def initlializeWalls(self):
        self.nOfAllWalls = self.nOfWalls + 2 * int(self.gameSizeX / 8) + 2 * int(self.gameSizeY / 8)
        for i in range(int(self.gameSizeX / 8)):
            self.walls.append(Wall(i * 8, 0))
            self.walls.append(Wall(i * 8, self.gameSizeY - 8))

        for i in range(int(self.gameSizeY / 8)):
            self.walls.append(Wall(0, i * 8))
            self.walls.append(Wall(self.gameSizeX - 8, i * 8))

        for i in range(self.nOfWalls):
            Xrand = int(random.randrange(1, (self.gameSizeX / 8) - 1))
            Yrand = int(random.randrange(1, (self.gameSizeY / 8) - 1))
            self.walls.append(Wall(Xrand * 8, Yrand * 8))

        self.nOfSideWalls = self.nOfAllWalls - self.nOfWalls

    def drawWalls(self):
        for i in range(self.nOfAllWalls):
            self.walls[i].draw()

    def checkCollision(self, obj):
        x = obj.x
        y = obj.y

        if pyxel.btnp(pyxel.KEY_DOWN):
            y += obj.h
            direction = Direction.DOWN

        elif pyxel.btnp(pyxel.KEY_UP):
            y -= obj.h
            direction = Direction.UP

        elif pyxel.btnp(pyxel.KEY_LEFT):
            x -= obj.w
            direction = Direction.LEFT

        elif pyxel.btnp(pyxel.KEY_RIGHT):
            x += obj.w
            direction = Direction.RIGHT

        for i in range(self.nOfAllWalls):
            if self.walls[i].x == x and self.walls[i].y == y:
                print()
                print(i)
                if i < self.nOfSideWalls:
                    return True
                else:
                    if self.checkCollision(self.walls[i]):
                        return True
                    else:
                        self.walls[i].moveWall(direction)
        return False


App()
