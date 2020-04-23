#
# Adrianna Rodencal
#
# Final Project for Programming 1
# Simon Memory Game
#
# Started: 12/3.19
# Last Updated: 13/3/19
#
import random, sys, time, pygame
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWLENGTH = 480
FLASHSPEED = 500
FLASHDELAY = 200
FPSCLOCK = pygame.time.Clock()
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
DISPLAYSURF = pygame.display.set_mode((WINDOWLENGTH, WINDOWWIDTH))
TIMEOUT = 5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) /2)
YMARGIN = int((WINDOWLENGTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) /2)

YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    pygame.font.init()
    basicFont = pygame.font.SysFont('Times New Romans', 20, False, False)
    size = (WINDOWWIDTH, WINDOWLENGTH)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Memory')
    infoSurf = basicFont.render('Click on the buttons that flash, in the order that they flash to level up.', 1, WHITE)
    infoLocation = (10, WINDOWLENGTH - 25)
    screen.blit(infoSurf, infoLocation)
    pygame.display.update()
    clock = pygame.time.Clock()
    print_instructions()
    gameData = init_game_data()
    computerPattern = []
    currentButton = 0
    score = 0
    inputWait = False
    while True:
        clickedButton = None
        DISPLAYSURF.fill(bgColor)
        drawButtons()
        scoreSurf = basicFont.render('Score: ' +str(score), 1, WHITE)
        scoreLocation = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreLocation)
        DISPLAYSURF.blit(infoSurf, infoLocation)
        clickedButton = event_handler(pygame, clickedButton)
        if inputWait == False:
            pygame.display.update()
            pygame.time.wait(1000)
            computerPattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in computerPattern:
                buttonFlash(button)
                pygame.time.wait(FLASHDELAY)
            inputWait = True
        else:
            if clickedButton and clickedButton == computerPattern[currentButton]:
                buttonFlash(clickedButton)
                currentButton += 1
                lastClickTime = time.time()
                if currentButton == len(computerPattern):
                    score += 1
                    inputWait = False
                    currentButton = 0
            elif (clickedButton and clickedButton != computerPattern[currentButton]) or (currentButton!= 0 and time.time() - TIMEOUT > lastClickTime):
                gameOver()
                #newRound = new_game('Would you like to play again?', basicFont)
                computerPattern = []
                currentButton = 0
                inputWait = False
                score = 0
                pygame.time.wait(1000)
    pygame.display.update()
    FPSCLOCK.tick(FPS)
                            

def print_instructions():
    print('''
Welcome to the wonderful game of Memory!! (I know, very creative title).
The game will start in a few short moments. Watch carefully and
try to remember the pattern of the flashing buttons.
Good Luck!''')
    

def init_game_data():
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Hello', 1, YELLOW)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWLENGTH - 25)
    
    pygame.display.update()

def event_handler(pygame, clickedButton):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            clickedButton = getButtonClicked(mouseX, mouseY)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                clickedButton = YELLOW
            elif event.key == pygame.K_w:
                clickedButton = BLUE
            elif event.key == pygame.K_a:
                clickedButton = RED
            elif event.key == pygame.K_s:
                clickedButton = GREEN
    return clickedButton

def terminate():
    pygame.quit()
    sys.exit()

def userQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def buttonFlash(color, animationSpeed = 50):
    if color == YELLOW:
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT

    originalSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    for start, end, step in((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed*step):
            userQuit()
            DISPLAYSURF.blit(originalSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(originalSurf, (0, 0))

def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)

def gameOver(color = WHITE, animationSpeed = 50):
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
                userQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                basicFont = pygame.font.SysFont('Times New Romans', 30, False, False)
                gameOver = basicFont.render('GAME OVER', 1, WHITE)
                endLocation = (255,0)
                DISPLAYSURF.blit(gameOver, endLocation)
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW
    elif BLUERECT.collidepoint((x, y)):
        return BLUE
    elif REDRECT.collidepoint((x, y)):
        return RED
    elif GREENRECT.collidepoint((x, y)):
        return GREEN
    return None

def new_game(prompt, basicFont):
    pygame.time.wait(1000)
    newGame = basicFont.render(prompt, 20, WHITE)
    questionLocation = (255, 232)
    DISPLAYSURF.blit(newGame, questionLocation)
    waitInfo = False
    while True:
        clickedButton = None
        redNo = basicFont.render('NO', 50, BLACK)
        greenYes = basicFont.render('YES', 50, BLACK)
        quitLocation = REDRECT
        continueLocation = GREENRECT
        DISPLAYSURF.blit(redNo, quitLocation)
        DISPLAYSURF.blit(greenYes, continueLocation)
        clickButton = event_handler(pygame, clickedButton)
        pygame.display.update()
        if waitInfo == False:
            if clickButton and clickButton == REDRECT:
                userQuit()
            elif clickButton and clickButton == continueLocation:
                return True



if __name__ == '__main__':
    main()
