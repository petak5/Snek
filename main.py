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
direction = "right"

screenWidth = 800
screenHeight = 600

fruitSize = 20

objSize = 20
#objWidth = 10
#objHeight = 10

sizeOfMove = objSize

gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Snek')

icon = pygame.image.load("snakeHead.png")
pygame.display.set_icon(icon)

img = pygame.image.load("snakeHead.png")
appleImg = pygame.image.load("apple.png")

clock = pygame.time.Clock()

smallFont = pygame.font.SysFont("comicsansms", 25)
mediumFont = pygame.font.SysFont("comicsansms", 50)
largeFont = pygame.font.SysFont("comicsansms", 80)

def pause():
    paused = True
    
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press P to continue, or Q to quit", black, 25, "small")
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)

def score(score):
    text = smallFont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, (0, 0))

def rand_apple_gen():
    randAppleX = round(random.randrange(0, screenWidth - fruitSize) / 10.0) * 10.0
    randAppleY = round(random.randrange(0, screenHeight - fruitSize) / 10.0) * 10.0
    return randAppleX, randAppleY

def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Wellcome to Snek", green, -100, "large")
        message_to_screen("The objective of the game is to eat red fruit", black, -30, "small")
        message_to_screen("The more apple you eat, the longer you get", black, 10, "small")
        message_to_screen("If you run into yourself, or the edges, you die!", black, 50, "small")
        message_to_screen("Press C to play, P to pause or Q to quit", black, 180, "small")

        pygame.display.update()
        clock.tick(15)

def snake(objSize, snakeList):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)

    if direction == "left":
        head = pygame.transform.rotate(img, 90)

    if direction == "up":
        head = img

    if direction == "bottom":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, darkerGreen, [XnY[0], XnY[1], objSize, objSize])

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    
    if size == "medium":
        textSurface = mediumFont.render(text, True, color)
    
    if size == "large":
        textSurface = largeFont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def message_to_screen(message, color, y_displace = 0, size = "small"):

    textSurface, textRectangle = text_objects(message, color, size)
    textRectangle.center = (screenWidth / 2, screenHeight / 2 + y_displace)
    gameDisplay.blit(textSurface, textRectangle)

def game_loop():
    global direction
    direction = "right"

    gameExit = False
    gameOver = False
    lead_x = screenWidth / 2
    lead_y = screenHeight / 2
    lead_x_change = 20
    lead_y_change = 0

    snakeList = []
    snakeLenght = 1

    # Generating random apple position and making it divisible by 10
    randAppleX, randAppleY = rand_apple_gen()


    # NEED TO FIX !

    # Making the apple divisible by objSize, so they perfectly align
    if (randAppleX % objSize != 0):
        randAppleX += (objSize - (randAppleY % objSize))

    if (randAppleY % objSize != 0):
        randAppleY += (objSize - (randAppleY % objSize))

    # While we don't want to exit game
    while not gameExit:

        if gameOver == True:
            message_to_screen("Game over", red, -50, "large")
            message_to_screen("press C to play again or Q to quit", black, 50, "medium")
            pygame.display.update()

        # Game over
        while gameOver == True:

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
                    direction = "left"
                    lead_x_change = -sizeOfMove
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = sizeOfMove
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_x_change = 0
                    lead_y_change = -sizeOfMove
                elif event.key == pygame.K_DOWN:
                    direction = "bottom"
                    lead_x_change = 0
                    lead_y_change = sizeOfMove
                elif event.key == pygame.K_p:
                    pause()

        # changing x and y position of the new block (head)
        lead_x += lead_x_change
        lead_y += lead_y_change

        # check of wall collision
        if lead_x < 0 or lead_x + objSize > screenWidth or lead_y < 0 or lead_y + objSize > screenHeight:
            gameOver = True


        # wiping board
        gameDisplay.fill(white)
        
        # drawing apple
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, fruitSize, fruitSize])
        gameDisplay.blit(appleImg, (randAppleX, randAppleY))

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

        score(snakeLenght - 1)

        pygame.display.update()

        # # collision logic, kinda
        # if lead_x == randAppleX and lead_y == randAppleY:
        #     print("I gotcha")
        #     randAppleX = round(random.randrange(0, screenWidth - objSize) / 10.0) * 10.0
        #     randAppleY = round(random.randrange(0, screenHeight - objSize) / 10.0) * 10.0
        #     snakeLenght += 1

        # more complex collision logic, which is not working well
        # need more work, but we dont need it for this simple snake
        if lead_x >= randAppleX and lead_x <= randAppleX + fruitSize or lead_x + objSize >= randAppleX and lead_x + objSize <= randAppleX + fruitSize:
            if lead_y >= randAppleY and lead_y <= randAppleY + fruitSize or lead_y + objSize >= randAppleY and lead_y + objSize <= randAppleY + fruitSize:

                randAppleX, randAppleY = rand_apple_gen()
                snakeLenght += 1

                # Making the apple divisible by objSize, so they perfectly align
                if (randAppleX % objSize
                 != 0):
                    randAppleX += (objSize - (randAppleY % objSize))

                if (randAppleY % objSize != 0):
                    randAppleY += (objSize - (randAppleY % objSize))

        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
game_loop()