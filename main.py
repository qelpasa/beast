import pyxel
import enum
import time
import random


# paste into terminal to enter pyxel editor
# pyxeleditor resources.pyres.pyxres
# TODO
# trapped enemy causes error
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

    def draw(self, BeastLevel):
        if BeastLevel == 1:
            pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h)
        elif BeastLevel == 2:
            pyxel.blt(self.x, self.y, 0, 32, 0, self.w, self.h)
        elif BeastLevel == 3:
            pyxel.blt(self.x, self.y, 0, 40, 0, self.w, self.h)
        else:
            pyxel.blt(self.x, self.y, 0, 48, 0, self.w, self.h)

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

        self.walls = []
        self.nOfWalls = 100
        self.nOfHardWalls = 15
        self.nOfSideWalls = 0
        self.nOfAllWalls = 0

        self.enemy1lvl = []
        self.enemy2lvl = []
        self.enemy3lvl = []
        self.enemy4lvl = []

        self.nOf1LvlEnemies = 2
        self.nOf2LvlEnemies = 0
        self.nOf3LvlEnemies = 0
        self.nOf4LvlEnemies = 0  # mines

        self.nOf1LvlEnemiesBuff = self.nOf1LvlEnemies
        self.nOf2LvlEnemiesBuff = self.nOf2LvlEnemies
        self.nOf3LvlEnemiesBuff = self.nOf3LvlEnemies
        self.nOf4LvlEnemiesBuff = self.nOf4LvlEnemies

        self.max1lvlEnemies = 5
        self.max2lvlEnemies = 3
        self.max3lvlEnemies = 1
        self.max4lvlEnemies = 5  # mines

        self.nOfEnemies = self.nOf1LvlEnemies
        self.nOfEnemiesBuff = self.nOfEnemies
        self.maxNumOfEnemies = self.max1lvlEnemies + self.max2lvlEnemies + self.max3lvlEnemies + self.max4lvlEnemies

        self.parity = 1
        self.endGame = False
        self.Menu = False
        self.speed = 1
        self.level = 1
        self.hardModeLevel = 5

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

            for i in range(self.nOf1LvlEnemies):
                if self.parity == 3:  # every third move make "intelligent" move
                    self.moveEnemy(i, lvl=1, moveTowardsPlayer=True)
                    self.parity = 1
                else:
                    self.moveEnemy(i, lvl=1)
                    self.parity += 1

                self.timeSinceLastMove = 0

            for i in range(self.nOf2LvlEnemies):
                if self.parity == 3:  # every third move make non "intelligent" move
                    self.moveEnemy(i, lvl=2)
                    self.parity = 1
                else:
                    self.moveEnemy(i, lvl=2, moveTowardsPlayer=True)
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
            self.drawEnemies()

            self.DrawLevel(self.level)
            self.DrawNOfBeasts(self.nOfEnemies)

    def DrawGameOver(self):
        pyxel.blt(90, 50, 0, 0, 8, 72, 16)

    def drawEnemies(self):
        for i in range(self.nOf1LvlEnemies):
            self.enemy1lvl[i].draw(1)

        for i in range(self.nOf2LvlEnemies):
            self.enemy2lvl[i].draw(2)

    def movePlayer(self):
        if not self.checkCollision(self.player, whatObj="player"):
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.player.y += self.player.h
            elif pyxel.btnp(pyxel.KEY_UP):
                self.player.y -= self.player.h
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.player.x -= self.player.w
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.player.x += self.player.w

            for j in range(self.nOf1LvlEnemies):
                if self.player.x == self.enemy1lvl[j].x and self.player.y == self.enemy1lvl[j].y:
                    self.endGame = True
            for j in range(self.nOf2LvlEnemies):
                if self.player.x == self.enemy2lvl[j].x and self.player.y == self.enemy2lvl[j].y:
                    self.endGame = True
            for j in range(self.nOf3LvlEnemies):
                if self.player.x == self.enemy3lvl[j].x and self.player.y == self.enemy3lvl[j].y:
                    self.endGame = True
            for j in range(self.nOf4LvlEnemies):
                if self.player.x == self.enemy4lvl[j].x and self.player.y == self.enemy4lvl[j].y:
                    self.endGame = True

        if pyxel.btnp(pyxel.KEY_1):
            self.enemy1lvl.pop(0)
            self.nOf1LvlEnemies -= 1
            self.nOfEnemies -= 1
            if self.nOfEnemies == 0:
                self.NextLevel()

        if pyxel.btnp(pyxel.KEY_2):
            self.enemy2lvl.pop(0)
            self.nOf2LvlEnemies -= 1
            self.nOfEnemies -= 1
            if self.nOfEnemies == 0:
                self.NextLevel()

    def initializeObjects(self):  # walls, enemies and player
        self.timeSinceLastMove = -1
        self.walls = []
        self.enemy1lvl = []
        self.enemy2lvl = []
        self.enemy3lvl = []
        self.enemy4lvl = []
        maxSizeX = int(self.gameSizeX / 8) - 1
        maxSizeY = int(self.gameSizeY / 8) - 1

        if self.level >= 2:
            playerPosX = self.player.x / 8
            playerPosY = self.player.y / 8
        else:
            playerPosX = int(self.playerInitPos / 8)
            playerPosY = playerPosX

        while len(self.walls) < self.nOfHardWalls:  # hard walls
            Xrand = int(random.randrange(1, maxSizeX))
            Yrand = int(random.randrange(1, maxSizeY))
            add = True
            if not (Xrand == playerPosX and Yrand == playerPosY):
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
            Xrand = int(random.randrange(1, maxSizeX))
            Yrand = int(random.randrange(1, maxSizeY))
            add = True
            if not (Xrand == playerPosX and Yrand == playerPosY):
                for i in range(len(self.walls)):
                    if self.walls[i].x == Xrand * 8 and self.walls[i].y == Yrand * 8:
                        add = False
                if add:
                    self.walls.append(Wall(Xrand * 8, Yrand * 8))

        self.nOfSideWalls = self.nOfAllWalls - self.nOfWalls

        self.player = Player(playerPosX * 8, playerPosY * 8)

        self.initializeEnemies(playerPosX, playerPosY)

        self.nOfEnemies = self.nOf1LvlEnemiesBuff + self.nOf2LvlEnemiesBuff + self.nOf3LvlEnemiesBuff + self.nOf4LvlEnemiesBuff

    def initializeEnemies(self, playerPosX, playerPosY):
        self.nOf1LvlEnemies = self.nOf1LvlEnemiesBuff
        self.nOf2LvlEnemies = self.nOf2LvlEnemiesBuff
        self.nOf3LvlEnemies = self.nOf3LvlEnemiesBuff
        self.nOf4LvlEnemies = self.nOf4LvlEnemiesBuff

        maxSizeX = int(self.gameSizeX / 8) - 1
        maxSizeY = int(self.gameSizeY / 8) - 1

        while len(self.enemy1lvl) < self.nOf1LvlEnemies:
            Xrand = 8 * int(random.randrange(1, maxSizeX))
            Yrand = 8 * int(random.randrange(1, maxSizeY))

            self.enemy1lvl.append(Enemy(Xrand, Yrand))
            for j in range(self.nOfAllWalls):
                if self.isPlayerAround(Xrand, Yrand, playerPosX, playerPosY, j):
                    self.enemy1lvl.pop()

        while len(self.enemy2lvl) < self.nOf2LvlEnemies:
            Xrand = 8 * int(random.randrange(1, maxSizeX))
            Yrand = 8 * int(random.randrange(1, maxSizeY))

            self.enemy2lvl.append(Enemy(Xrand, Yrand))
            for j in range(self.nOfAllWalls):
                if self.isPlayerAround(Xrand, Yrand, playerPosX, playerPosY, j):
                    self.enemy2lvl.pop()

        while len(self.enemy3lvl) < self.nOf3LvlEnemies:
            Xrand = 8 * int(random.randrange(1, maxSizeX))
            Yrand = 8 * int(random.randrange(1, maxSizeY))

            self.enemy3lvl.append(Enemy(Xrand, Yrand))
            for j in range(self.nOfAllWalls):
                if self.isPlayerAround(Xrand, Yrand, playerPosX, playerPosY, j):
                    self.enemy3lvl.pop()

        while len(self.enemy4lvl) < self.nOf4LvlEnemies:
            Xrand = 8 * int(random.randrange(1, maxSizeX))
            Yrand = 8 * int(random.randrange(1, maxSizeY))

            self.enemy4lvl.append(Enemy(Xrand, Yrand))
            for j in range(self.nOfAllWalls):
                if self.isPlayerAround(Xrand, Yrand, playerPosX, playerPosY, j):
                    self.enemy4lvl.pop()

    def moveEnemy(self, whichEnemy, lvl, moveTowardsPlayer=False):
        if lvl == 1:
            if moveTowardsPlayer:
                verticalOrHorizontalMove = random.randint(0, 1)
                if verticalOrHorizontalMove == 0:
                    if self.player.x > self.enemy1lvl[whichEnemy].x:
                        move = Direction.RIGHT
                    else:
                        move = Direction.LEFT
                else:
                    if self.player.y > self.enemy1lvl[whichEnemy].y:
                        move = Direction.DOWN
                    else:
                        move = Direction.UP
            else:
                move = random.choice(list(Direction))

            if self.checkCollision(self.enemy1lvl[whichEnemy], "enemy", EnemyDirection=move):
                self.enemy1lvl[whichEnemy].moveEnemy(move)
            else:
                self.moveEnemy(whichEnemy, 1)

            for i in range(self.nOf1LvlEnemies):  # check for losing the game
                if self.player.x == self.enemy1lvl[i].x and self.player.y == self.enemy1lvl[i].y:
                    self.endGame = True

        if lvl == 2:
            if moveTowardsPlayer:
                verticalOrHorizontalMove = random.randint(0, 1)
                if verticalOrHorizontalMove == 0:
                    if self.player.x > self.enemy2lvl[whichEnemy].x:
                        move = Direction.RIGHT
                    else:
                        move = Direction.LEFT
                else:
                    if self.player.y > self.enemy2lvl[whichEnemy].y:
                        move = Direction.DOWN
                    else:
                        move = Direction.UP
            else:
                move = random.choice(list(Direction))

            if self.checkCollision(self.enemy2lvl[whichEnemy], "enemy", EnemyDirection=move):
                print("enemy: ", whichEnemy)
                self.enemy2lvl[whichEnemy].moveEnemy(move)
            else:
                self.moveEnemy(whichEnemy, lvl=2)

            for i in range(self.nOf2LvlEnemies):  # check for losing the game
                if self.player.x == self.enemy2lvl[i].x and self.player.y == self.enemy2lvl[i].y:
                    self.endGame = True

        if lvl == 3:
            if moveTowardsPlayer:
                verticalOrHorizontalMove = random.randint(0, 1)
                if verticalOrHorizontalMove == 0:
                    if self.player.x > self.enemy3lvl[whichEnemy].x:
                        move = Direction.RIGHT
                    else:
                        move = Direction.LEFT
                else:
                    if self.player.y > self.enemy3lvl[whichEnemy].y:
                        move = Direction.DOWN
                    else:
                        move = Direction.UP
            else:
                move = random.choice(list(Direction))

            if self.checkCollision(self.enemy3lvl[whichEnemy], "enemy", EnemyDirection=move):
                print("enemy: ", whichEnemy)
                self.enemy3lvl[whichEnemy].moveEnemy(move)
            else:
                self.moveEnemy(whichEnemy, lvl=3)

            for i in range(self.nOf3LvlEnemies):  # check for losing the game
                if self.player.x == self.enemy3lvl[i].x and self.player.y == self.enemy3lvl[i].y:
                    self.endGame = True

        if lvl == 4:
            if moveTowardsPlayer:
                verticalOrHorizontalMove = random.randint(0, 1)
                if verticalOrHorizontalMove == 0:
                    if self.player.x > self.enemy4lvl[whichEnemy].x:
                        move = Direction.RIGHT
                    else:
                        move = Direction.LEFT
                else:
                    if self.player.y > self.enemy4lvl[whichEnemy].y:
                        move = Direction.DOWN
                    else:
                        move = Direction.UP
            else:
                move = random.choice(list(Direction))

            if self.checkCollision(self.enemy4lvl[whichEnemy], "enemy", EnemyDirection=move):
                print("enemy: ", whichEnemy)
                self.enemy4lvl[whichEnemy].moveEnemy(move)
            else:
                self.moveEnemy(whichEnemy, lvl=4)

            for i in range(self.nOf4LvlEnemies):  # check for losing the game
                if self.player.x == self.enemy4lvl[i].x and self.player.y == self.enemy4lvl[i].y:
                    self.endGame = True

    def drawWalls(self):
        for i in range(self.nOfHardWalls):
            self.walls[i].draw(ifHard=True)

        for i in range(self.nOfHardWalls, self.nOfAllWalls):
            self.walls[i].draw()

    def checkCollision(self, obj, whatObj="notEnemy", EnemyDirection=-1):  # True for no collision
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

    def isPlayerAround(self, Xrand, Yrand, playerPosX, playerPosY, j):
        if ((self.walls[j].x == Xrand and self.walls[j].y == Yrand) or
                (Xrand == playerPosX + 1 and Yrand == playerPosY) or
                (Xrand == playerPosX - 1 and Yrand == playerPosY) or
                (Xrand == playerPosX and Yrand == playerPosY) or
                (Xrand == playerPosX + 1 and Yrand == playerPosY + 1) or
                (Xrand == playerPosX - 1 and Yrand == playerPosY + 1) or
                (Xrand == playerPosX and Yrand == playerPosY + 1) or
                (Xrand == playerPosX + 1 and Yrand == playerPosY - 1) or
                (Xrand == playerPosX - 1 and Yrand == playerPosY - 1) or
                (Xrand == playerPosX and Yrand == playerPosY - 1)):
            return True
        else:
            return False

    def executeEnemies(self):
        self.execute1lvlEnemies()
        self.execute2lvlEnemies()
        self.execute3lvlEnemies()
        self.execute4lvlEnemies()

    def execute1lvlEnemies(self):
        continueLoops = True
        for i in range(self.nOf1LvlEnemies):
            if continueLoops:
                for j in range(self.nOfAllWalls):
                    if continueLoops:
                        if self.walls[j].x == self.enemy1lvl[i].x and self.walls[j].y == self.enemy1lvl[i].y:
                            self.enemy1lvl.pop(i)
                            self.nOf1LvlEnemies -= 1
                            self.nOfEnemies -= 1
                            continueLoops = False
                            break
        if self.nOfEnemies == 0:
            self.NextLevel()

    def execute2lvlEnemies(self):
        continueLoops = True
        for i in range(self.nOf2LvlEnemies):
            if continueLoops:
                for j in range(self.nOfAllWalls):
                    if continueLoops:
                        if self.walls[j].x == self.enemy2lvl[i].x and self.walls[j].y == self.enemy2lvl[i].y:
                            self.enemy2lvl.pop(i)
                            self.nOf2LvlEnemies -= 1
                            self.nOfEnemies -= 1
                            continueLoops = False
                            break
        if self.nOfEnemies == 0:
            self.NextLevel()

    def execute3lvlEnemies(self):
        continueLoops = True
        for i in range(self.nOf3LvlEnemies):
            if continueLoops:
                for j in range(self.nOfAllWalls):
                    if continueLoops:
                        if self.walls[j].x == self.enemy3lvl[i].x and self.walls[j].y == self.enemy3lvl[i].y:
                            self.enemy3lvl.pop(i)
                            self.nOf3LvlEnemies -= 1
                            self.nOfEnemies -= 1
                            continueLoops = False
                            break
        if self.nOfEnemies == 0:
            self.NextLevel()

    def execute4lvlEnemies(self):
        continueLoops = True
        for i in range(self.nOf4LvlEnemies):
            if continueLoops:
                for j in range(self.nOfAllWalls):
                    if continueLoops:
                        if self.walls[j].x == self.enemy4lvl[i].x and self.walls[j].y == self.enemy4lvl[i].y:
                            self.enemy4lvl.pop(i)
                            self.nOf4LvlEnemies -= 1
                            self.nOfEnemies -= 1
                            continueLoops = False
                            break
        if self.nOfEnemies == 0:
            self.NextLevel()

    def NextLevel(self):

        self.level += 1

        if self.nOf1LvlEnemiesBuff < self.max1lvlEnemies:
            self.nOf1LvlEnemiesBuff += 1

        if self.level >= self.hardModeLevel:
            if self.nOf2LvlEnemiesBuff < self.max2lvlEnemies:
                self.nOf2LvlEnemiesBuff += 1

        self.initializeObjects()
        self.endGame = False
        self.speed *= 0.9
        print("level: ", self.level)

    def DrawLevel(self, level):
        levelText = "Level " + str(level)
        pyxel.rect(8, 0, len(levelText) * pyxel.FONT_WIDTH + 1, 8, 5)
        pyxel.text(9, 1, levelText, 7)

    def DrawNOfBeasts(self, number):
        levelText = "Beasts " + str(number)
        pyxel.rect(48, 0, len(levelText) * pyxel.FONT_WIDTH + 1, 8, 5)
        pyxel.text(49, 1, levelText, 7)


App()
