# Author: Bhaskar Tallamraju
# Date  : 24 Sep 2020

import os
import sys
import time
import random
from math import *
from enum import Enum
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.locals import *
from pygame.draw import rect
from pygame.sprite import RenderUpdates

# CONSTANTS
GAME_SCORE = 11
GAME_MAX_LEVEL = 3
LENGTH_OF_PADDLE = 100
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
BG_COLOR = (23, 57, 75)
LIGHT_GREY = (200, 200, 200)
LIGHT_RED = (200, 0, 0)
LIGHT_GREEN = (0, 200, 0)
LIGHT_BLUE = (0, 0, 200)
BLUE = (118, 155, 175)
WHITE = (255, 255, 255)
DARK_WINDOW = (82, 85, 82)
SKY_COLOR = (0, 0, 173)
GOR_COLOR = (255, 170, 82)
BAN_COLOR = (255, 255, 82)
EXPLOSION_COLOR = (255, 0, 0)
SUN_COLOR = (255, 255, 0)
DARK_RED_COLOR = (173, 0, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
GRAY_COLOR = (173, 170, 173)

BALL_SPEED = 6
PADDLE_SPEED = 5

class GameParams:
    """ Stores game parameters """
    def __init__(self):
        self.level = 1
        self.Game_Score = 11
        self.score_time = True
        self.best_left_score = [0, 0]
        self.best_right_score = [0, 0]
        self.left_wins = 0
        self.right_wins = 0
        self.len_of_paddle = 100
        self.pong_sound = None
        self.score_sound = None
        self.ball = None
        self.ball_speed_x = BALL_SPEED * random.choice((1, -1))
        self.ball_speed_y = BALL_SPEED * random.choice((1, -1))
        self.best_left_level = 0
        self.best_right_level = 0

class Player:
    """ Stores information about a player """
    def __init__(self, score=0, two_player=False, current_level=1, Right_Name="RIGHT PLAYER", Left_Name="LEFT PLAYER"):
        self.score = score
        self.two_player = two_player
        self.current_level = current_level
        self.Left_Name = Left_Name
        self.Right_Name = Right_Name
        self.leftPlayer_speed = 0
        self.rightPlayer_speed = 0
        self.leftPlayer_score = 0
        self.rightPlayer_score = 0
        self.leftPlayer = None
        self.rightPlayer = None

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    image = image.convert()

    return image, image.get_rect()

def getModCase(s, mod):
    """Checks the state of the shift and caps lock keys, and switches the case of the s string if needed."""
    if bool(mod & KMOD_RSHIFT or mod & KMOD_LSHIFT) ^ bool(mod & KMOD_CAPS):
        return s.swapcase()
    else:
        return s

def drawText(text, surfObj, x, y, fgcol, bgcol, pos='left'):
    #GAME_FONT = pygame.font.SysFont(None, 20)
    GAME_FONT = pygame.font.Font("freesansbold.ttf", 25)

    textobj = GAME_FONT.render(text, 1, fgcol, bgcol) # creates the text in memory (it's not on a surface yet).
    textrect = textobj.get_rect()

    if pos == 'left':
        textrect.topleft = (int(x), int(y))
    elif pos == 'center':
        textrect.midtop = (int(x), int(y))
    surfObj.blit(textobj, textrect) # draws the text onto the surface
    return textrect

def inputMode(prompt, screenSurf, x, y, fgcol, bgcol, maxlen=12, allowed=None, pos='left', cursor='_', cursorBlink=False):
    FPS = 30
    GAME_CLOCK = pygame.time.Clock()
    inputText = ''
    """inputText will store the text of what the player has typed in so far."""
    done = False
    cursorTimestamp = time.time()
    cursorShow = cursor
    while not done:
        if cursor and cursorBlink and time.time() - 1.0 > cursorTimestamp:
            if cursorShow == cursor:
                cursorShow = '   '
            else:
                cursorShow = cursor
            cursorTimestamp = time.time()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return None
                elif event.key == K_RETURN:
                    done = True
                    if cursorShow:
                        cursorShow = '   '
                elif event.key == K_BACKSPACE:
                    if len(inputText):
                        drawText(prompt + inputText + cursorShow, screenSurf, textrect.left, textrect.top, bgcol, bgcol, 'left')
                        inputText = inputText[:-1]
                else:
                    if len(inputText) >= maxlen or (allowed is not None and chr(event.key) not in allowed):
                        continue
                    if event.key >= 32 and event.key < 128:
                        inputText += getModCase(chr(event.key), event.mod)

        textrect = drawText(prompt + cursorShow, screenSurf, x, y, fgcol, bgcol, pos)
        drawText(prompt + inputText + cursorShow, screenSurf, textrect.left, textrect.top, fgcol, bgcol, 'left')
        pygame.display.update()
        GAME_CLOCK.tick(FPS)
    return inputText

def waitForPlayerToPressKey():
    """Calling this function will pause the program until the user presses a key. The key is returned."""
    while True:
        key = checkForKeyPress()
        if key:
            return key

def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE: # pressing escape quits
                terminate()
            return event.key
    return False

class Head(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('assets/pong.jpg', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.STEP = BALL_SPEED
        self.MARGIN = 300
        self.xstep = self.STEP
        self.ystep = 0
        self.degrees = 0
        self.direction = 'right'

    def update(self):
        if self.degrees:
            self._spin()
        else:
            self._move()

    def _move(self):
        newpos = self.rect.move((self.xstep, self.ystep))

        if self.direction == 'right' and self.rect.right > self.area.right - self.MARGIN:
            self.xstep = -self.STEP
            self.ystep = 3
            self.direction = 'left'

        if self.direction == 'left' and self.rect.left < self.area.left + self.MARGIN:
            self.xstep = self.STEP
            self.ystep = -3
            self.direction = 'right'
        '''
        if self.direction == 'right' and self.rect.right > self.area.right - self.MARGIN:
            self.xstep = -2
            self.ystep = self.STEP
            self.direction = 'down'

        if self.direction == 'down' and self.rect.bottom > self.area.bottom - self.MARGIN:
            self.xstep = -self.STEP
            self.ystep = 1
            self.direction = 'left'

        if self.direction == 'left' and self.rect.left < self.area.left + self.MARGIN:
            self.xstep = 2
            self.ystep = -self.STEP
            self.direction = 'up'

        if self.direction == 'up' and self.rect.top < self.area.top + self.MARGIN:
            self.xstep = self.STEP
            self.ystep = -1
            self.direction = 'right'
        '''

        self.rect = newpos

    def _spin(self):
        center = self.rect.center
        self.degrees = self.degrees + 12
        if self.degrees >= 360:
            self.degrees = 0
            self.image = self.original
        else:
            self.image = pygame.transform.rotate(self.original, self.degrees)
        self.rect = self.image.get_rect(center=center)

    def hit(self):
        if not self.degrees:
            self.degrees = 1
            self.original = self.image

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    ONE_PLAYER = 1
    TWO_PLAYER = 2
    HELP = 3
    BACK = 4
    HELP_LT = 5
    HELP_RT = 6
    TOPSCORE = 7


class Screen():
    def __init__(self, screen, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen

class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)
