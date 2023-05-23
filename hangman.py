#########################################################
##              File Name: hangman.py                  ##
#########################################################
import pygame
import sys
import random
from pygame import mixer
# pygame for interactive ui and random for random word choosing
# mixer for loading and playing music

pygame.init()  # this initializes the pygame variables
winHeight = 480
winWidth = 700  ##we've  defined height and width of the window
win = pygame.display.set_mode((winWidth, winHeight))
# ---------------------------------------#
# initialize global variables/constants #
# ---------------------------------------#

# # Starting the mixer
mixer.init()
# Loading the song
mixer.music.load("mix_4m35s (audio-joiner.com).mp3")
#
# # Setting the volume
mixer.music.set_volume(0.7)
#
# # Start playing the song
mixer.music.play()

bgimg = pygame.image.load('ACU.jpg')
bgimg = pygame.transform.scale(bgimg, (winWidth, winHeight)).convert_alpha()  # so that

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("comicsansms", 35)
lost_font = pygame.font.SysFont('timesnewroman', 35)
# we also have to create different font objects of different
# fonts , size  for different purposes eg like the title would be displayed
# larger on the screen and words will be a bit smaller

word = ''
buttons = []
guessed = []
hangmanPics = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    hangmanPics.append(image)
# we have to create object for images we  have 7 images so we create images list
# and store each image in it using for loop

limbs = 0


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(WHITE)
    win.blit(bgimg, (0, 0))
    # Buttons
    for i in range(len(buttons)):  ## for all 26 buttons
        if buttons[i][4]:  ## if its visible draw it
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])  ## x , y and radius
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]),
                               buttons[i][3] - 2)  ## for background of buttons
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, WHITE)
    rect = label1.get_rect()
    length = rect[2]

    win.blit(label1, (winWidth / 2 - length / 2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth / 2 - pic.get_width() / 2 + 20, 150))
    pygame.display.update()


## for random word
def randomWord():
    file = open('words.txt')
    f = file.readlines()  ## creates an array of all the lines
    i = random.randrange(0,len(f) - 1)  # The randrange() method returns a
                # randomly selected element from the specified range in this (0,len(f)-1)

    return f[i][:-1]  ## this to not include the \n in end of every line


def hang(guess):
    global word
    if guess.lower() not in word.lower():  ## returns true when guess not in word
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(
                    len(guessedLetters)):  # so if its not a spacebar then we
                # replace it by _ else we replace it by the letter(ie A) if it has already been guessed
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '  ## if its a space then add space to the word
    return spacedWord


def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:  ## ie return if button hit
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'  ## by default winner is false
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(WHITE)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)  ## if won display win text and vice versa

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth / 2 - wordTxt.get_width() / 2, 295))
    win.blit(wordWas, (winWidth / 2 - wordWas.get_width() / 2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    quit=0
    while again:
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                again = False
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.KEYDOWN:  ## if a key is pressed then we go to reset
                again = False

    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):  ## all are made visible
        buttons[i][4] = True

    limbs = 0  ## limbs changed to 0
    guessed = []  ## guessed again changed to []
    word = randomWord()  ## choose a random word


# MAINLINE


# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)  ## 2 rows and 13  columns
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

word = randomWord()  ## now we initialize or get a random word
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False  ## if either escape is pressed or quit we quit
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()

# always quit pygame when done!


