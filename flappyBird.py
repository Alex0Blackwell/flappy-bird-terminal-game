import time, random, os, keyboard

# install keyboard, needs sudo

w, h = 100, 10;
firstPipePos = score = 0;
birdYPos = h//2
pipeSplitsQueue = []
gameBoard = [[0 for x in range(w)] for y in range(h)]
collision = False


def rbgToAnsii(word, r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m{word}\x1b[0m"


class Game():
    """docstring for Game."""

    def drawPipe(self, xpos, split):
        '''width of 2, opening of 3 above the split, removes previous pipe'''

        for i in range(h):
            if(not(split-3 <= i <= split)):
                gameBoard[i][xpos] = rbgToAnsii('@', 116, 191, 46)
                if(xpos+1 < w):
                    gameBoard[i][xpos+1] = rbgToAnsii('@', 116, 191, 46)
                    if(xpos+2 < w):
                        gameBoard[i][xpos+2] = f"{rbgToAnsii('-', 113, 197, 207) if (i < 8) else rbgToAnsii('=', 221, 216, 148)}"

    def deletePipe(self, xpos):
        for i in range(h):
            gameBoard[i][xpos] = f"{rbgToAnsii('-', 113, 197, 207) if (i < 8) else rbgToAnsii('=', 221, 216, 148)}"
            gameBoard[i][xpos+1] = f"{rbgToAnsii('-', 113, 197, 207) if (i < 8) else rbgToAnsii('=', 221, 216, 148)}"

    def startGame(self):

        global firstPipePos, pipeSplitsQueue
        pipeSplitsQueue = []
        for i in range(h):
            for j in range(w):
                gameBoard[i][j] = f"{rbgToAnsii('-', 113, 197, 207) if (i < 8) else rbgToAnsii('=', 221, 216, 148)}"
        # spawn 4 pipes every
        firstPipePos = 15
        for i in range(15, 100, 15):
            split = random.randint(5, 8)
            pipeSplitsQueue.append(split)
            thisPipe = Game()
            thisPipe.drawPipe(i, split)

    def printFrame(self):
        for i in range(h):
            res = ""
            for j in range(w):
                # print('\033[07m', end='')  # reverse colours
                res += '\033[07m'+gameBoard[i][j]
            print(res)

    def updatePipes(self, frames):
        '''update pipes every 3th frame, spawn in new pipes, spawn out old pipes'''
        if(frames % 3 == 0):
            global score
            global firstPipePos
            firstPipePos -= 1

            if(firstPipePos == 5):
                score += 1

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
        body = rbgToAnsii('#', 249, 241, 36)
        front = rbgToAnsii('\\', 249, 241, 36)
        beak = rbgToAnsii('>', 250, 103, 75)
        for i in range(h):
            for j in range(x, x+3):
                coor = gameBoard[i][j]
                if(coor == body or coor == front or coor == beak):
                    gameBoard[i][j] = f"{rbgToAnsii('-', 113, 197, 207) if (i < 8) else rbgToAnsii('=', 221, 216, 148)}"

        # check for collision on this bird
        # top = gameBoard[y-1][x]
        # topR = gameBoard[y-1][x+1]
        coor = gameBoard[y][x]
        right = gameBoard[y][x+1]
        twoR = gameBoard[y][x+2]
        pole = rbgToAnsii('@', 116, 191, 46)

        if(coor == pole or right == pole or twoR == pole):
            global collision
            collision = True

        mainBody = rbgToAnsii('#', 249, 241, 36)
        # gameBoard[y-1][x] = mainBody # above
        gameBoard[y][x] = mainBody  # at coordinate
        gameBoard[y][x+1] = mainBody  # right
        # gameBoard[y-1][x+1] = rbgToAnsii('\\', 249, 241, 36) # above'\\'  # above right
        gameBoard[y][x+2] = rbgToAnsii('>', 250, 103, 75)  # two right



    def gravity(self):# \x1b[38;2;{r};{g};{b}m{darkToBright[totalBrightness//70]}\x1b[0m
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

    global collision, score
    jumped = endGame = scoreUpdated = False
    frames = 1
    frameTime = 0.2  # time for each frame
    while(not endGame):
        score = 0
        game = Game()
        bird = Bird()
        game.startGame()
        bird.drawBird(5, birdYPos)
        while(not collision and not endGame):
            scoreUpdated = False
            os.system('cls' if os.name == 'nt' else 'clear')
            if(not jumped):
                bird.gravity()

            game.updatePipes(frames)
            game.printFrame()

            frames += 1
            if(frames == 1000):
                # to rid overflow potential
                frames = 1

            print(f"Your score is {score}!\n")

            print("Press \"e\" to end the round")
            print("Press space to jump! ")
            t0 = time.time()
            jumped = False
            while(time.time()-t0 < frameTime):
                if keyboard.is_pressed(' '):
                    jumped = True;
                    bird.jump()
                    break;
                elif keyboard.is_pressed('e'):
                    endGame = True
                    break

            wait = round(time.time()-t0, 2)
            # floating point errors if we dont round
            time.sleep(frameTime-wait)

        if(collision):
            print("\nWhoops, you had a collision!")
        userIn = input("\nType \"end\" to end the game, press \"enter\" to play again:\n")
        if("end" in userIn):
            endGame = True
        else:
            collision = endGame = False


if __name__ == '__main__':
    main()
