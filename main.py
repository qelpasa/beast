import pyxel
import enum
import time
import random


# paste into terminal to enter pyxel editor
# pyxeleditor resources.pyres.pyxres

# TODO
# Best perks
# cant exit game in main menu
# some animations of level transitions, to main menu (between screens)


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

    def Draw(self, ifHard=False):
        if ifHard:
            pyxel.blt(self.x, self.y, 0, 24, 0, self.w, self.h)
        else:
            pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h)

    def MoveWall(self, direction):
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

    def Draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8

    def Draw(self, beastLevel):
        if beastLevel == 1:
            pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h)
        elif beastLevel == 2:
            pyxel.blt(self.x, self.y, 0, 32, 0, self.w, self.h)
        elif beastLevel == 3:
            pyxel.blt(self.x, self.y, 0, 40, 0, self.w, self.h)
        else:
            pyxel.blt(self.x, self.y, 0, 48, 0, self.w, self.h)

    def MoveEnemy(self, direction):
        if direction == Direction.LEFT:
            self.x -= self.w
        elif direction == Direction.RIGHT:
            self.x += self.w
        elif direction == Direction.UP:
            self.y -= self.h
        elif direction == Direction.DOWN:
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

        self.init1lvlEnemies = 2
        self.init2lvlEnemies = 0
        self.init3lvlEnemies = 0
        self.init4lvlEnemies = 0  # mines

        self.nOf1LvlEnemies = self.init1lvlEnemies
        self.nOf2LvlEnemies = self.init2lvlEnemies
        self.nOf3LvlEnemies = self.init3lvlEnemies
        self.nOf4LvlEnemies = self.init4lvlEnemies

        self.nOf1LvlEnemiesBuff = self.init1lvlEnemies
        self.nOf2LvlEnemiesBuff = self.init2lvlEnemies
        self.nOf3LvlEnemiesBuff = self.init3lvlEnemies
        self.nOf4LvlEnemiesBuff = self.init4lvlEnemies

        self.max1lvlEnemies = 5
        self.max2lvlEnemies = 3
        self.max3lvlEnemies = 1
        self.max4lvlEnemies = 5  # mines

        self.nOfEnemies = self.nOf1LvlEnemies
        self.nOfEnemiesBuff = self.nOfEnemies
        self.maxNumOfEnemies = self.max1lvlEnemies + self.max2lvlEnemies + self.max3lvlEnemies + self.max4lvlEnemies

        self.parity = 1
        self.endGame = False
        self.menu = True
        self.menuButton = 1

        self.initSpeed = 1
        self.initMultiplier = 1.1
        self.speedlvl = []
        self.speedlvl.append(self.initSpeed)
        self.speedlvl.append(self.initMultiplier * self.speedlvl[0])
        self.speedlvl.append(self.initMultiplier * self.speedlvl[1])

        self.level = 1
        self.hardModeLevel = 5

        pyxel.init(self.gameSizeX, self.gameSizeY, scale=5, caption="BEAST", fps=60)
        pyxel.load("assets/resources.pyres.pyxres")

        self.timeLastFrame = []
        self.dt = []
        self.timeSinceLastMove = []

        for i in range(4):
            self.timeLastFrame.append(time.time())
            self.dt.append(0)
            self.timeSinceLastMove.append(0)

        pyxel.run(self.UpdateMenu, self.DrawMenu)

    def UpdateMenu(self):
        if not self.menu:
            pyxel.run(self.Update, self.Draw)

        if pyxel.btnp(pyxel.KEY_UP):
            if self.menuButton == 3:
                self.menuButton = 1
            else:
                self.menuButton += 1

        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.menuButton == 1:
                self.menuButton = 3
            else:
                self.menuButton -= 1

        if pyxel.btnp(pyxel.KEY_ENTER):
            if self.menuButton == 1:
                self.ResetValues()
                self.InitializeObjects()
                self.menu = False
            elif self.menuButton == 2:
                print("Authors")
            else:
                quit()  # TODO how to exit??

    def DrawMenu(self):
        pyxel.rect(0, 0, self.gameSizeX, self.gameSizeY, 1)

        if self.menuButton == 1:
            text1 = 10
            text2 = 7
            text3 = 7
        elif self.menuButton == 2:
            text1 = 7
            text2 = 10
            text3 = 7
        else:
            text1 = 7
            text2 = 7
            text3 = 10

        pyxel.text(int(self.gameSizeX / 2) - 30, int(self.gameSizeY / 2 - 20), "NewGame", text1)
        pyxel.text(int(self.gameSizeX / 2) - 30, int(self.gameSizeY / 2) + 8, "Creators", text2)
        pyxel.text(int(self.gameSizeX / 2) - 30, int(self.gameSizeY / 2) - 6, "Press Esc to exit", text3)

    def Update(self):
        if self.menu:
            pyxel.run(self.UpdateMenu, self.DrawMenu)

        self.MovePlayer()
        self.ExecuteEnemies()
        timeThisFrame = []

        for i in range(4):
            timeThisFrame.append(time.time())
            self.dt[i] = timeThisFrame[i] - self.timeLastFrame[i]
            self.timeLastFrame[i] = timeThisFrame[i]
            self.timeSinceLastMove[i] += self.dt[i]

        if self.timeSinceLastMove[0] >= self.speedlvl[0]:
            for i in range(self.nOf1LvlEnemies):
                if self.parity == 3:  # every third move make move towards player
                    self.MoveEnemy(i, lvl=1, moveTowardsPlayer=True)
                    self.parity = 1
                else:
                    self.MoveEnemy(i, lvl=1)
                    self.parity += 1

            self.timeSinceLastMove[0] = 0

        if self.timeSinceLastMove[1] >= self.speedlvl[1]:
            for i in range(self.nOf2LvlEnemies):
                if self.parity == 2:  # every second move make move towards player
                    self.MoveEnemy(i, lvl=2)
                    self.parity = 1
                else:
                    self.MoveEnemy(i, lvl=2, moveTowardsPlayer=True)
                    self.parity += 1

            self.timeSinceLastMove[1] = 0

        if self.timeSinceLastMove[2] >= self.speedlvl[2]:
            for i in range(self.nOf3LvlEnemies):  # every move towards player
                self.MoveEnemy(i, lvl=3, moveTowardsPlayer=True)

            self.timeSinceLastMove[2] = 0

        if pyxel.btnp(pyxel.KEY_R):
            self.InitializeObjects()
            self.endGame = False

        elif pyxel.btnp(pyxel.KEY_Q):
            self.menu = True

        elif pyxel.btnp(pyxel.KEY_1):
            self.enemy1lvl.pop(0)
            self.nOf1LvlEnemies -= 1
            self.nOfEnemies -= 1

        elif pyxel.btnp(pyxel.KEY_2):
            self.enemy2lvl.pop(0)
            self.nOf2LvlEnemies -= 1
            self.nOfEnemies -= 1

        elif pyxel.btnp(pyxel.KEY_3):
            self.enemy3lvl.pop(0)
            self.nOf3LvlEnemies -= 1
            self.nOfEnemies -= 1

        elif pyxel.btnp(pyxel.KEY_4):
            self.enemy4lvl.pop(0)
            self.nOf4LvlEnemies -= 1
            self.nOfEnemies -= 1

    def Draw(self):
        if self.endGame:
            pyxel.cls(0)
            self.DrawGameOver()
        else:
            pyxel.cls(0)
            self.DrawWalls()
            self.player.Draw()
            self.DrawEnemies()

            self.DrawLevel(self.level)
            self.DrawNOfBeasts(self.nOfEnemies)

    def InitializeObjects(self):  # walls, enemies and player
        for i in range(4):
            self.timeSinceLastMove[i] = -0.5

        self.speedlvl[1] = 0.9 * self.speedlvl[0]
        self.speedlvl[2] = 0.9 * self.speedlvl[1]

        self.walls = []
        self.enemy1lvl = []
        self.enemy2lvl = []
        self.enemy3lvl = []
        self.enemy4lvl = []  # mines

        maxSizeX = int(self.gameSizeX / 8) - 1
        maxSizeY = int(self.gameSizeY / 8) - 1

        if self.level >= 2:  # gets players last position
            playerPosX = self.player.x / 8
            playerPosY = self.player.y / 8
        else:
            playerPosX = int(self.playerInitPos / 8)
            playerPosY = playerPosX

        while len(self.walls) < self.nOfHardWalls:  # hard walls (yellow)
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

        while len(self.walls) < self.nOfAllWalls:  # normal walls
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

        self.InitializeEnemies()

    def InitializeEnemies(self):
        self.nOf1LvlEnemies = self.nOf1LvlEnemiesBuff
        self.nOf2LvlEnemies = self.nOf2LvlEnemiesBuff
        self.nOf3LvlEnemies = self.nOf3LvlEnemiesBuff
        self.nOf4LvlEnemies = self.nOf4LvlEnemiesBuff

        maxSizeX = int(self.gameSizeX / 8) - 1
        maxSizeY = int(self.gameSizeY / 8) - 1

        while len(self.enemy1lvl) < self.nOf1LvlEnemies:
            Xrand = int(random.randrange(1, maxSizeX))
            Yrand = int(random.randrange(1, maxSizeY))

            self.enemy1lvl.append(Enemy(Xrand * 8, Yrand * 8))
            for j in range(self.nOfAllWalls):
                if self.IsPlayerAround(Xrand, Yrand, j):
                    self.enemy1lvl.pop()
                    break

        while len(self.enemy2lvl) < self.nOf2LvlEnemies:
            Xrand = int(random.randrange(1, maxSizeX))
            Yrand = int(random.randrange(1, maxSizeY))

            self.enemy2lvl.append(Enemy(Xrand * 8, Yrand * 8))
            for j in range(self.nOfAllWalls):
                if self.IsPlayerAround(Xrand, Yrand, j):
                    self.enemy2lvl.pop()
                    break

        while len(self.enemy3lvl) < self.nOf3LvlEnemies:
            Xrand = int(random.randrange(1, maxSizeX))
            Yrand = int(random.randrange(1, maxSizeY))

            self.enemy3lvl.append(Enemy(Xrand * 8, Yrand * 8))
            for j in range(self.nOfAllWalls):
                if self.IsPlayerAround(Xrand, Yrand, j):
                    self.enemy3lvl.pop()
                    break

        while len(self.enemy4lvl) < self.nOf4LvlEnemies:
            Xrand = int(random.randrange(1, maxSizeX))
            Yrand = int(random.randrange(1, maxSizeY))

            self.enemy4lvl.append(Enemy(Xrand * 8, Yrand * 8))
            for j in range(self.nOfAllWalls):
                if self.IsPlayerAround(Xrand, Yrand, j):
                    self.enemy4lvl.pop()
                    break

        self.nOfEnemies = self.nOf1LvlEnemiesBuff + self.nOf2LvlEnemiesBuff + self.nOf3LvlEnemiesBuff + self.nOf4LvlEnemiesBuff

    def IsPlayerAround(self, Xrand, Yrand, j):
        PlayerPosX = int(self.player.x / 8)
        PlayerPosY = int(self.player.y / 8)
        if int(self.walls[j].x / 8) == Xrand and int(self.walls[j].y / 8) == Yrand:  # if enemy spawns on walls
            return True
        elif PlayerPosX == Xrand and PlayerPosY == Yrand:  # if enemy spawns on player
            return True
        else:
            return False

    def MovePlayer(self):
        if not self.CheckCollision(self.player, whatObj="player"):
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.player.y += self.player.h
            elif pyxel.btnp(pyxel.KEY_UP):
                self.player.y -= self.player.h
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.player.x -= self.player.w
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.player.x += self.player.w

            for j in range(self.nOf1LvlEnemies):  # check losing game after player move
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

    def MoveEnemy(self, whichEnemy, lvl, moveTowardsPlayer=False):
        if lvl == 1:
            self.MoveEnemyLevel(whichEnemy, lvl, moveTowardsPlayer, self.enemy1lvl, self.nOf1LvlEnemies)

        elif lvl == 2:
            self.MoveEnemyLevel(whichEnemy, lvl, moveTowardsPlayer, self.enemy2lvl, self.nOf2LvlEnemies)

        elif lvl == 3:
            self.MoveEnemyLevel(whichEnemy, lvl, moveTowardsPlayer, self.enemy3lvl, self.nOf3LvlEnemies)

    def MoveEnemyLevel(self, whichEnemy, lvl, moveTowardsPlayer, obj, nOfEnemies):
        if moveTowardsPlayer:
            verticalOrHorizontalMove = random.randint(0, 1)
            if verticalOrHorizontalMove == 0:
                if self.player.x > obj[whichEnemy].x:
                    move = Direction.RIGHT
                else:
                    move = Direction.LEFT
            else:
                if self.player.y > obj[whichEnemy].y:
                    move = Direction.DOWN
                else:
                    move = Direction.UP
        else:
            move = random.choice(list(Direction))

        if self.CheckCollision(obj[whichEnemy], "enemy", EnemyDirection=move):
            obj[whichEnemy].MoveEnemy(move)
        else:  # make no move when trapped
            if self.CheckCollision(obj[whichEnemy], "enemy", EnemyDirection=Direction.LEFT) or \
                    self.CheckCollision(obj[whichEnemy], "enemy", EnemyDirection=Direction.RIGHT) or \
                    self.CheckCollision(obj[whichEnemy], "enemy", EnemyDirection=Direction.UP) or \
                    self.CheckCollision(obj[whichEnemy], "enemy", EnemyDirection=Direction.DOWN):
                self.MoveEnemy(whichEnemy, lvl)

        for i in range(nOfEnemies):  # check losing game after enemy move
            if self.player.x == obj[i].x and self.player.y == obj[i].y:
                self.endGame = True

    def CheckCollision(self, obj, whatObj="notEnemy", EnemyDirection=-1):  # True for no collision
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
        else:  # player or wall
            for i in range(self.nOfAllWalls):
                if self.walls[i].x == x and self.walls[i].y == y:
                    if self.level >= self.hardModeLevel and whatObj == "player":  # game over when stepped on yellow
                        if i < self.nOfHardWalls:  # wall becomes explosive after certain level
                            self.endGame = True
                            self.DrawGameOver()
                            return False
                    if i < self.nOfSideWalls:
                        return True
                    else:
                        if self.CheckCollision(self.walls[i]):
                            return True
                        else:
                            self.walls[i].MoveWall(direction)
        return False

    def ExecuteEnemies(self):
        self.Execute1lvlEnemies()
        self.Execute2lvlEnemies()
        self.Execute3lvlEnemies()
        self.Execute4lvlEnemies()

        if self.nOfEnemies == 0:
            self.NextLevel()

    def Execute1lvlEnemies(self):
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

    def Execute2lvlEnemies(self):
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

    def Execute3lvlEnemies(self):
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

    def Execute4lvlEnemies(self):
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

    def NextLevel(self):
        self.level += 1

        if self.nOf1LvlEnemiesBuff < self.max1lvlEnemies:
            self.nOf1LvlEnemiesBuff += 1

        if self.level >= self.hardModeLevel:
            if self.nOf2LvlEnemiesBuff < self.max2lvlEnemies:
                self.nOf2LvlEnemiesBuff += 1

        if self.level >= self.hardModeLevel + self.max2lvlEnemies + self.max3lvlEnemies + 2:
            if self.nOf3LvlEnemiesBuff < self.max3lvlEnemies:
                self.nOf3LvlEnemiesBuff += 1

        if self.level >= self.hardModeLevel + self.max2lvlEnemies + self.max3lvlEnemies:  # mines
            if self.nOf4LvlEnemiesBuff < self.max4lvlEnemies:
                self.nOf4LvlEnemiesBuff += 1

        self.speedlvl[0] *= 0.9
        self.InitializeObjects()
        self.endGame = False

    def DrawLevel(self, level):
        levelText = "Level " + str(level)
        pyxel.rect(8, 0, len(levelText) * pyxel.FONT_WIDTH + 1, 8, 5)
        pyxel.text(9, 1, levelText, 7)

    def DrawNOfBeasts(self, number):
        levelText = "Beasts " + str(number)
        pyxel.rect(48, 0, len(levelText) * pyxel.FONT_WIDTH + 1, 8, 5)
        pyxel.text(49, 1, levelText, 7)

    def DrawWalls(self):
        for i in range(self.nOfHardWalls):
            self.walls[i].Draw(ifHard=True)

        for i in range(self.nOfHardWalls, self.nOfAllWalls):
            self.walls[i].Draw()

    def DrawGameOver(self):
        pyxel.rect(0, 0, self.gameSizeX, self.gameSizeY, 1)
        pyxel.text(int(self.gameSizeX / 2) - 19, int(self.gameSizeY / 2 - 20), "GAME OVER", 7)
        pyxel.text(int(self.gameSizeX / 2) - 39, int(self.gameSizeY / 2 - 10), "(PRESS 'R' TO RESET)", 7)

    def DrawEnemies(self):
        for i in range(self.nOf1LvlEnemies):
            self.enemy1lvl[i].Draw(beastLevel=1)

        for i in range(self.nOf2LvlEnemies):
            self.enemy2lvl[i].Draw(beastLevel=2)

        for i in range(self.nOf3LvlEnemies):
            self.enemy3lvl[i].Draw(beastLevel=3)

        for i in range(self.nOf4LvlEnemies):
            self.enemy4lvl[i].Draw(beastLevel=4)

    def ResetValues(self):
        self.level = 1
        self.nOf1LvlEnemiesBuff = self.init1lvlEnemies
        self.nOf2LvlEnemiesBuff = self.init2lvlEnemies
        self.nOf3LvlEnemiesBuff = self.init3lvlEnemies
        self.nOf4LvlEnemiesBuff = self.init4lvlEnemies  # mines

        self.nOfEnemies = self.nOf1LvlEnemies
        self.nOfEnemiesBuff = self.nOfEnemies
        self.maxNumOfEnemies = self.max1lvlEnemies + self.max2lvlEnemies + self.max3lvlEnemies + self.max4lvlEnemies
        self.endGame = False
        self.menuButton = 1

        self.speedlvl = []
        self.speedlvl.append(self.initSpeed)
        self.speedlvl.append(self.initMultiplier * self.speedlvl[0])
        self.speedlvl.append(self.initMultiplier * self.speedlvl[1])


App()
