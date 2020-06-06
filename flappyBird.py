import time, random, os, keyboard

# install keyboard, needs sudo

w, h = 100, 10;
gameBoard = [[0 for x in range(w)] for y in range(h)]
birdYPos = h//2
firstPipePos = 0;
pipeSplitsQueue = []
collision = False

class Game():
    """docstring for Game."""

    def drawPipe(self, xpos, split):
        '''width of 2, opening of 3 above the split, removes previous pipe'''

        for i in range(h):
            if(not(split-3 <= i <= split)):
                gameBoard[i][xpos] = '@'
                if(xpos+1 < w):
                    gameBoard[i][xpos+1] = '@'
                    if(xpos+2 < w):
                        gameBoard[i][xpos+2] = f"{'-' if (i < 8) else '='}"

    def deletePipe(self, xpos):
        for i in range(h):
            gameBoard[i][xpos] = f"{'-' if (i < 8) else '='}"
            gameBoard[i][xpos+1] = f"{'-' if (i < 8) else '='}"

    def startGame(self):

        global firstPipePos, pipeSplitsQueue
        pipeSplitsQueue = []
        for i in range(h):
            for j in range(w):
                gameBoard[i][j] = f"{'-' if (i < 8) else '='}"
        # spawn 4 pipes every
        firstPipePos = 15
        for i in range(15, 100, 15):
            split = random.randint(5, 8)
            pipeSplitsQueue.append(split)
            thisPipe = Game()
            thisPipe.drawPipe(i, split)

    def printFrame(self):
        for i in range(h):
            print(''.join(gameBoard[i]))

    def updatePipes(self, frames):
        '''update pipes every 3th frame, spawn in new pipes, spawn out old pipes'''
        if(frames % 3 == 0):
            global firstPipePos
            firstPipePos -= 1
            if(firstPipePos < 0):
                # this pipe must get removed
                thisPipe = Game()
                thisPipe.deletePipe(firstPipePos+1)
                firstPipePos += 15
                pipeSplitsQueue.pop(0)
            c = 0
            for i in range(firstPipePos, w, 15):
                thisPipe = Game()
                if(c < len(pipeSplitsQueue)):
                    thisPipe.drawPipe(i, pipeSplitsQueue[c])
                else:
                    # a new pipe needs to be generated
                    split = random.randint(5, 8)
                    pipeSplitsQueue.append(split)
                    thisPipe.drawPipe(i, split)
                c += 1



class Bird():
    """docstring for Bird."""


    def drawBird(self, x, y):
        '''note the bird requires the space above it'''
        global birdYPos
        birdYPos = y
        # first clear the bird before
        for i in range(h):
            for j in range(x, x+3):
                coor = gameBoard[i][j]
                if(coor == '#' or coor == '\\' or coor == '>'):
                    gameBoard[i][j] = f"{'-' if (i < 8) else '='}"

        # check for collision on this bird
        top = gameBoard[y-1][x]
        topR = gameBoard[y-1][x+1]
        coor = gameBoard[y][x]
        right = gameBoard[y][x+1]
        twoR = gameBoard[y][x+2]

        if(top == '@' or topR == '@' or coor == '@' or right == '@' or twoR == '@'):
            global collision
            collision = True

        gameBoard[y-1][x] = '#'  # above
        gameBoard[y-1][x+1] = '\\'  # above right
        gameBoard[y][x] = '#'  # at coordinate
        gameBoard[y][x+1] = '#'  # right
        gameBoard[y][x+2] = '>'  # two right



    def gravity(self):
        '''drop the bird by a row'''
        dropBy = 1
        if(birdYPos+dropBy >= h):
            # on the ground
            dropBy = 0
        bird = Bird()
        bird.drawBird(5, birdYPos+dropBy)


    def jump(self):
        '''raise the bird by a row'''
        raiseby = 0
        if(birdYPos > 1):
            # roof check
            raiseby = 1
        bird = Bird()
        bird.drawBird(5, birdYPos-raiseby)



def main():

    global collision
    jumped = endGame = False
    frames = 1
    frameTime = 0.2  # time for each frame
    while(not endGame):
        game = Game()
        bird = Bird()
        game.startGame()
        while(not collision and not endGame):
            os.system('cls' if os.name == 'nt' else 'clear')
            if(not jumped):
                bird.gravity()
            else:
                bird.jump()
            game.updatePipes(frames)

            game.printFrame()

            frames += 1
            if(frames == 1000):
                # in case of overflow
                frames = 1
            print(frames)

            print("Press \"e\" to end the game")
            print("Press space to jump! ")
            t0 = time.time()
            jumped = False
            while(time.time()-t0 < frameTime):
                if keyboard.is_pressed(' '):
                    jumped = True;
                    break;
                elif keyboard.is_pressed('e'):
                    endGame = True

            wait = round(time.time()-t0, 2)
            # rounding errors if we dont round
            time.sleep(frameTime-wait)

        if(collision):
            print("whoops, you had a collision!")
        userIn = input("Type \"end\" to end the game, press \"enter\" to play again:\n")
        if("end" in userIn):
            endGame = True
        collision = False


if __name__ == '__main__':
    main()
