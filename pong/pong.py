import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates
from gameloop import *
from common import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

def title_screen(screen):
    screen_width = screen.screen_width
    screen_height = screen.screen_height

    one_player = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2-60)),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="ONE PLAYER",
        action=GameState.ONE_PLAYER,
    )
    two_player = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2)),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="TWO PLAYER",
        action=GameState.TWO_PLAYER,
    )
    quit_btn = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2+60)),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )
    help_btn = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2+120)),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Help",
        action=GameState.HELP,
    )

    buttons = RenderUpdates(one_player, two_player, quit_btn, help_btn)

    return game_loop(screen.screen, buttons)

def game_loop(screen, buttons):
    """ Handles game loop until an action is return by a button in the
        buttons sprite renderer.
    """
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

def help_screen(scr):
    screen = scr.screen
    HELP = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2)),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Right Player : UP and DOWN keys and Left Player : W and S keys",
        action=GameState.HELP,
    )

    buttons = RenderUpdates(HELP)
    return game_loop(screen, buttons)

def main():
    pygame.init()
    pygame.display.set_caption('Pong')

    screen = Screen(pygame.display.set_mode((screen_width, screen_height)))
    game_state = GameState.TITLE
    player = Player()

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.ONE_PLAYER:
            player.two_player = False
            game_state = play_pong(screen, player)

        if game_state == GameState.TWO_PLAYER:
            player.two_player = True
            game_state = play_pong(screen, player)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

        if game_state == GameState.HELP:
            player.two_player = True
            game_state = help_screen(screen)

if __name__ == "__main__":
    main()
