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


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h)

    def moveEnemy(self, direction):
        if direction == Direction.LEFT:
            self.x -= self.w
        if direction == Direction.RIGHT:
            self.x += self.w
        if direction == Direction.UP:
            self.y -= self.h
        if direction == Direction.DOWN:
            self.y += self.h


class App:
    def __init__(self):
        self.playerInitPos = 32
        self.gameSizeX = 256
        self.gameSizeY = 120
        self.nOfWalls = 41
        self.nOfAllWalls = 0
        self.nOfSideWalls = 0

        pyxel.init(self.gameSizeX, self.gameSizeY, scale=5, caption="NIBBLES", fps=60)
        pyxel.load("assets/resources.pyres.pyxres")

        self.initlializeWalls()

        self.timeLastFrame = time.time()
        self.dt = 0
        self.timeSinceLastMove = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.initlializeWalls()

        self.movePlayer()

        timeThisFrame = time.time()
        self.dt = timeThisFrame - self.timeLastFrame
        self.timeLastFrame = timeThisFrame
        self.timeSinceLastMove += self.dt

        if self.timeSinceLastMove >= 0.3:  # speed
            self.moveEnemy()
            self.timeSinceLastMove = 0

    def draw(self):
        pyxel.cls(0)
        self.drawWalls()
        self.player.draw()
        self.enemy.draw()

    def movePlayer(self):
        if not self.checkCollision(self.player, "player"):
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.player.y += self.player.h
            elif pyxel.btnp(pyxel.KEY_UP):
                self.player.y -= self.player.h
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.player.x -= self.player.w
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.player.x += self.player.w
        if pyxel.btnp(pyxel.KEY_SPACE):
            print("x")

    def initlializeWalls(self):
        self.walls = []

        self.nOfAllWalls = self.nOfWalls + 2 * int(self.gameSizeX / 8) + 2 * int(self.gameSizeY / 8)
        for i in range(int(self.gameSizeX / 8)):
            self.walls.append(Wall(i * 8, 0))
            self.walls.append(Wall(i * 8, self.gameSizeY - 8))

        for i in range(int(self.gameSizeY / 8)):
            self.walls.append(Wall(0, i * 8))
            self.walls.append(Wall(self.gameSizeX - 8, i * 8))

        wallsToDelete = 0
        for i in range(self.nOfWalls):
            Xrand = int(random.randrange(1, (self.gameSizeX / 8) - 1))
            Yrand = int(random.randrange(1, (self.gameSizeY / 8) - 1))

            playerPos = int(self.playerInitPos / 8)

            if Xrand == playerPos and Yrand == playerPos:
                wallsToDelete += 1
            else:
                self.walls.append(Wall(Xrand * 8, Yrand * 8))

        self.nOfAllWalls -= wallsToDelete
        self.nOfWalls -= wallsToDelete
        self.nOfSideWalls = self.nOfAllWalls - self.nOfWalls

        self.player = Player(self.playerInitPos, self.playerInitPos)
        self.enemy = Enemy(48, 48)

    def moveEnemy(self):
        move = random.choice(list(Direction))

        if self.checkCollision(self.enemy, "enemy", EnemyDirection=move):
            self.enemy.moveEnemy(move)

        # for i in range(self.nOfAllWalls):

    def drawWalls(self):
        for i in range(self.nOfAllWalls):
            self.walls[i].draw()

    def checkCollision(self, obj, whatObj, EnemyDirection=-1):
        x = obj.x
        y = obj.y
        print(x, " ", y)
        if pyxel.btnp(pyxel.KEY_DOWN) or EnemyDirection == Direction.DOWN:
            y += obj.h
            direction = Direction.DOWN

        elif pyxel.btnp(pyxel.KEY_UP) or EnemyDirection == Direction.UP:
            y -= obj.h
            direction = Direction.UP

        elif pyxel.btnp(pyxel.KEY_LEFT) or EnemyDirection == Direction.LEFT:
            x -= obj.w
            direction = Direction.LEFT

        elif pyxel.btnp(pyxel.KEY_RIGHT) or EnemyDirection == Direction.RIGHT:
            x += obj.w
            direction = Direction.RIGHT


        if whatObj == "enemy":
            print(x, " ", y)
            print(EnemyDirection)
            for i in range(self.nOfAllWalls):
                if self.walls[i].x == x and self.walls[i].y == y:
                    return False
            return True
        else:
            for i in range(self.nOfAllWalls):
                if self.walls[i].x == x and self.walls[i].y == y:
                    if i < self.nOfSideWalls:
                        return True
                    else:
                        if self.checkCollision(self.walls[i], "wall"):
                            return True
                        else:
                            self.walls[i].moveWall(direction)

        return False


App()
