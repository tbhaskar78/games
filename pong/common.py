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
BALL_SPEED = 6
PADDLE_SPEED = 5

class GameParams:
    """ Stores game parameters """
    def __init__(self):
        self.level = 1
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
