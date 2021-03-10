import pyxel
import enum
import time
import random


# paste into terminal to enter pyxel editor
# pyxeleditor resources.pyres.pyxres
# TODO
# trapped enemy causes error
# level name on screen
# Best perks

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

    def draw(self, ifHard=False):
        if ifHard:
            pyxel.blt(self.x, self.y, 0, 24, 0, self.w, self.h)
        else:
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

    def draw(self, ifBeast=False):
        if ifBeast:
            pyxel.blt(self.x, self.y, 0, 32, 0, self.w, self.h)
        else:
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
        self.enemy = []
        self.walls = []
        self.playerInitPos = 32
        self.gameSizeX = 256
        self.gameSizeY = 120
        self.nOfWalls = 60
        self.nOfHardWalls = 9
        self.nOfSideWalls = 0
        self.nOfAllWalls = 0
        self.nOfEnemies = 2
        self.maxNumOfEnemies = 5
        self.nOfEnemiesBuff = self.nOfEnemies
        self.parity = 1
        self.endGame = False
        self.Menu = False
        self.speed = 1
        self.level = 1
        self.hardModeLevel = 5
        self.level_text = ""

        pyxel.init(self.gameSizeX, self.gameSizeY, scale=5, caption="BEAST", fps=60)
        pyxel.load("assets/resources.pyres.pyxres")

        self.initializeObjects()

        self.timeLastFrame = time.time()
        self.dt = 0
        self.timeSinceLastMove = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        self.movePlayer()
        self.executeEnemies()
        timeThisFrame = time.time()
        self.dt = timeThisFrame - self.timeLastFrame
        self.timeLastFrame = timeThisFrame
        self.timeSinceLastMove += self.dt

        if self.timeSinceLastMove >= self.speed:

            for i in range(self.nOfEnemies):
                if self.parity == 2:  # every second move make "intelligent" move
                    self.moveEnemy(i, moveTowardsPlayer=True)
                    self.parity = 1
                else:
                    self.moveEnemy(i)
                    self.parity += 1

                self.timeSinceLastMove = 0

        if pyxel.btnp(pyxel.KEY_R):
            self.initializeObjects()
            self.endGame = False

    def draw(self):
        if self.endGame:
            pyxel.cls(0)
            self.DrawGameOver()
        else:
            pyxel.cls(0)
            self.drawWalls()
            self.player.draw()
            for i in range(self.nOfEnemies):
                if self.level >= self.hardModeLevel:
                    self.enemy[i].draw(ifBeast=True)
                else:
                    self.enemy[i].draw()
            self.DrawLevel(self.level)
            self.DrawBeasts(self.nOfEnemies)

    def DrawGameOver(self):
        pyxel.blt(90, 50, 0, 0, 8, 72, 16)

    def movePlayer(self):
        if not self.checkCollision(self.player, whatObj="player"):
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.player.y += self.player.h
                print(self.player.x, ",", self.player.y)
            elif pyxel.btnp(pyxel.KEY_UP):
                self.player.y -= self.player.h
                print(self.player.x, ",", self.player.y)
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.player.x -= self.player.w
                print(self.player.x, ",", self.player.y)
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.player.x += self.player.w
                print(self.player.x, ",", self.player.y)

            for i in range(self.nOfEnemies):
                if self.player.x == self.enemy[i].x and self.player.y == self.enemy[i].y:
                    self.endGame = True

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.enemy.pop(0)
            self.nOfEnemies -= 1

    def initializeObjects(self):  # walls, enemies and player

        playerPos = int(self.playerInitPos / 8)

        while len(self.walls) < self.nOfHardWalls:  # hard walls
            Xrand = int(random.randrange(1, (self.gameSizeX / 8) - 1))
            Yrand = int(random.randrange(1, (self.gameSizeY / 8) - 1))
            add = True
            if not (Xrand == playerPos and Yrand == playerPos):
                if len(self.walls) >= 1:
                    for i in range(len(self.walls)):
                        if self.walls[i].x == Xrand * 8 and self.walls[i].y == Yrand * 8:
                            add = False
                    if add:
                        self.walls.append(Wall(Xrand * 8, Yrand * 8))
                else:
                    self.walls.append(Wall(Xrand * 8, Yrand * 8))

        self.nOfAllWalls = self.nOfWalls + 2 * int(self.gameSizeX / 8) + 2 * int(self.gameSizeY / 8) + self.nOfHardWalls

        for i in range(int(self.gameSizeX / 8)):  # vertical walls
            self.walls.append(Wall(i * 8, 0))
            self.walls.append(Wall(i * 8, self.gameSizeY - 8))

        for i in range(int(self.gameSizeY / 8)):  # horizontal walls
            self.walls.append(Wall(0, i * 8))
            self.walls.append(Wall(self.gameSizeX - 8, i * 8))

        while len(self.walls) < self.nOfAllWalls:  # hard walls
            Xrand = int(random.randrange(1, (self.gameSizeX / 8) - 1))
            Yrand = int(random.randrange(1, (self.gameSizeY / 8) - 1))
            add = True
            if not (Xrand == playerPos and Yrand == playerPos):
                for i in range(len(self.walls)):
                    if self.walls[i].x == Xrand * 8 and self.walls[i].y == Yrand * 8:
                        add = False
                if add:
                    self.walls.append(Wall(Xrand * 8, Yrand * 8))

        self.nOfSideWalls = self.nOfAllWalls - self.nOfWalls

        self.player = Player(self.playerInitPos, self.playerInitPos)

        self.nOfEnemies = self.nOfEnemiesBuff

        while len(self.enemy) < self.nOfEnemies:
            Xrand = 8 * int(random.randrange(1, (self.gameSizeX / 8) - 1))
            Yrand = 8 * int(random.randrange(1, (self.gameSizeY / 8) - 1))

            self.enemy.append(Enemy(Xrand, Yrand))
            for j in range(self.nOfAllWalls):
                if (self.walls[j].x == Xrand and self.walls[j].y == Yrand) or (
                        Xrand == playerPos and Yrand == playerPos):
                    self.enemy.pop(len(self.enemy) - 1)

    def moveEnemy(self, whichEnemy, moveTowardsPlayer=False):
        if moveTowardsPlayer:
            verticalOrHorizontalMove = random.randint(0, 1)
            if verticalOrHorizontalMove == 0:
                if self.player.x > self.enemy[whichEnemy].x:
                    move = Direction.RIGHT
                else:
                    move = Direction.LEFT
            else:
                if self.player.y > self.enemy[whichEnemy].y:
                    move = Direction.DOWN
                else:
                    move = Direction.UP
        else:
            move = random.choice(list(Direction))

        if self.checkCollision(self.enemy[whichEnemy], "enemy", EnemyDirection=move):
            self.enemy[whichEnemy].moveEnemy(move)
        else:
            self.moveEnemy(whichEnemy)

        for i in range(self.nOfEnemies):  # check for losing the game
            if self.player.x == self.enemy[i].x and self.player.y == self.enemy[i].y:
                self.endGame = True

    def drawWalls(self):
        for i in range(self.nOfHardWalls):
            self.walls[i].draw(ifHard=True)

        for i in range(self.nOfHardWalls, self.nOfAllWalls):
            self.walls[i].draw()

    def checkCollision(self, obj, whatObj="notEnemy", EnemyDirection=-1):
        x = obj.x
        y = obj.y

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
            for i in range(self.nOfAllWalls):
                if self.walls[i].x == x and self.walls[i].y == y:
                    return False
            return True
        else:
            for i in range(self.nOfAllWalls):
                if self.walls[i].x == x and self.walls[i].y == y:
                    if self.level >= self.hardModeLevel and whatObj == "player":  # game over when stepped on yellow
                        if i < self.nOfHardWalls:  # wall after certain level
                            self.endGame = True
                            self.DrawGameOver()
                            return False
                    if i < self.nOfSideWalls:
                        return True
                    else:
                        if self.checkCollision(self.walls[i]):
                            return True
                        else:
                            self.walls[i].moveWall(direction)
        return False

    def executeEnemies(self):
        continueLoops = True
        for i in range(self.nOfEnemies):
            if continueLoops:
                for j in range(self.nOfAllWalls):
                    if continueLoops:
                        if self.walls[j].x == self.enemy[i].x and self.walls[j].y == self.enemy[i].y:
                            self.enemy.pop(i)
                            self.nOfEnemies -= 1
                            continueLoops = False
                            break
        if self.nOfEnemies == 0:
            self.NextLevel()

    def NextLevel(self):

        if self.nOfEnemiesBuff < self.maxNumOfEnemies:
            self.nOfEnemiesBuff += 1
        self.initializeObjects()
        self.endGame = False
        self.speed *= 0.85
        self.level += 1
        print("level: ", self.level)

    def DrawLevel(self, level):
        self.level_text = "Level " + str(level)
        pyxel.rect(8, 0, len(self.level_text) * pyxel.FONT_WIDTH + 1, 8, 5)
        pyxel.text(9, 1, self.level_text, 7)

    def DrawBeasts(self, number):
        self.level_text = "Beasts " + str(number)
        pyxel.rect(48, 0, len(self.level_text) * pyxel.FONT_WIDTH + 1, 8, 5)
        pyxel.text(49, 1, self.level_text, 7)


App()
