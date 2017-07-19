import pygame, time, random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

darkerRed = (155, 0, 0)
darkerGreen = (0, 155, 0)
darkerBlue = (0, 0, 155)

FPS = 15

screenWidth = 800
screenHeight = 600

objSize = 10
#objWidth = 10
#objHeight = 10

sizeOfMove = 10

gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Snek')

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)

def snake(objSize, snakeList):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, darkerGreen, [XnY[0], XnY[1], objSize, objSize])

def message_to_screen(message, color):
    screen_text = font.render(message, True, color)
    gameDisplay.blit(screen_text, [screenWidth / 2, screenHeight / 2])

def game_loop():
    gameExit = False
    gameOver = False
    lead_x = screenWidth / 2
    lead_y = screenHeight / 2
    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLenght = 1

    fruitSize = 10

    randAppleX = round(random.randrange(0, screenWidth - objSize) / 10.0) * 10.0
    randAppleY = round(random.randrange(0, screenHeight - objSize) / 10.0) * 10.0

    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        game_loop()
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -sizeOfMove
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = sizeOfMove
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_x_change = 0
                    lead_y_change = -sizeOfMove
                elif event.key == pygame.K_DOWN:
                    lead_x_change = 0
                    lead_y_change = sizeOfMove




        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x < 0 or lead_x > screenWidth - objSize or lead_y < 0 or lead_y > screenHeight - objSize:
            gameOver = True



        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, fruitSize, fruitSize])

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLenght:
            del snakeList[0]

        for eachSegmen in snakeList[: -1]:
            if eachSegmen == snakeHead:
                gameOver = True

        snake(objSize, snakeList)

        pygame.display.update()

        if lead_x == randAppleX and lead_y == randAppleY:
            print("I gotcha")
            randAppleX = round(random.randrange(0, screenWidth - objSize) / 10.0) * 10.0
            randAppleY = round(random.randrange(0, screenHeight - objSize) / 10.0) * 10.0
            snakeLenght += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()