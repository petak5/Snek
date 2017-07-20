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

fruitSize = 20

objSize = 20
#objWidth = 10
#objHeight = 10

sizeOfMove = objSize

gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Snek')

img = pygame.image.load("snakeHead.png")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)

def snake(objSize, snakeList):
    gameDisplay.blit(img, (snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, darkerGreen, [XnY[0], XnY[1], objSize, objSize])

def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(message, color):
    # screen_text = font.render(message, True, color)
    # gameDisplay.blit(screen_text, [screenWidth / 2, screenHeight / 2])

    textSurface, textRectangle = text_objects(message, color)
    textRectangle.center = (screenWidth / 2, screenHeight / 2)
    gameDisplay.blit(textSurface, textRectangle)

def game_loop():
    gameExit = False
    gameOver = False
    lead_x = screenWidth / 2
    lead_y = screenHeight / 2
    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLenght = 1

    # Generating random apple position and making it divisible by 10
    randAppleX = round(random.randrange(0, screenWidth - objSize) / 10.0) * 10.0
    randAppleY = round(random.randrange(0, screenHeight - objSize) / 10.0) * 10.0


    # NEED TO FIX !

    # Making the apple divisible by objSize, so they perfectly align
    if (randAppleX % objSize != 0):
        randAppleX += (objSize - (randAppleY % objSize))

    if (randAppleY % objSize != 0):
        randAppleY += (objSize - (randAppleY % objSize))

    # While we don't want to exit game
    while not gameExit:

        # Game over
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit", red)
            pygame.display.update()

            # Events in game over menu
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

        # Game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            # Movement events
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

        # changing x and y position of the new block (head)
        lead_x += lead_x_change
        lead_y += lead_y_change

        # check of wall collision
        if lead_x < 0 or lead_x + objSize > screenWidth or lead_y < 0 or lead_y + objSize > screenHeight:
            gameOver = True


        # wiping board
        gameDisplay.fill(white)
        
        # drawing apple
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, fruitSize, fruitSize])

        # list of head's position
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)

        # appending head to the list of snake body
        # !! head is located at the end of the list !!
        snakeList.append(snakeHead)

        # deleting last element of snake (first of the list), unless snake eats fruit
        if len(snakeList) > snakeLenght:
            del snakeList[0]

        # checking of self collision
        for eachSegment in snakeList[: -1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(objSize, snakeList)

        pygame.display.update()

        # collision logic, kinda
        if lead_x == randAppleX and lead_y == randAppleY:
            print("I gotcha")
            randAppleX = round(random.randrange(0, screenWidth - objSize) / 10.0) * 10.0
            randAppleY = round(random.randrange(0, screenHeight - objSize) / 10.0) * 10.0
            snakeLenght += 1

        # # more complex collision logic, which is not working well
        # # need more work, but we dont need it for this simple snake
        # if lead_x >= randAppleX and lead_x <= randAppleX + fruitSize or lead_x + objSize >= randAppleX and lead_x + objSize <= randAppleX + fruitSize:
        #     if lead_y >= randAppleY and lead_y <= randAppleY + fruitSize or lead_y + objSize >= randAppleY and lead_y + objSize <= randAppleY + fruitSize:
        #         print("I gotcha")
        #         randAppleX = round(random.randrange(0, screenWidth - objSize) / 10.0) * 10.0
        #         randAppleY = round(random.randrange(0, screenHeight - objSize) / 10.0) * 10.0
        #         snakeLenght += 1



        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()