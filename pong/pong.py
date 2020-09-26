# Author: Bhaskar Tallamraju
# Date  : 24 Sep 2020

#!/usr/bin/env python3
from gameloop import *
from common import *


def title_screen(screen):
    screen_width = screen.screen_width
    screen_height = screen.screen_height

    one_player = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2)),
        font_size=30,
        bg_rgb=BG_COLOR,
        text_rgb=WHITE,
        text="ONE PLAYER",
        action=GameState.ONE_PLAYER,
    )
    two_player = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2)+60),
        font_size=30,
        bg_rgb=BG_COLOR,
        text_rgb=WHITE,
        text="TWO PLAYER",
        action=GameState.TWO_PLAYER,
    )
    topscore_btn = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2+120)),
        font_size=30,
        bg_rgb=BG_COLOR,
        text_rgb=WHITE,
        text="TOP SCORE",
        action=GameState.TOPSCORE,
    )
    help_btn = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2+180)),
        font_size=30,
        bg_rgb=BG_COLOR,
        text_rgb=WHITE,
        text="HELP",
        action=GameState.HELP,
    )
    quit_btn = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2+240)),
        font_size=30,
        bg_rgb=BG_COLOR,
        text_rgb=WHITE,
        text="EXIT",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(one_player, two_player, topscore_btn, quit_btn, help_btn)

    return game_loop(screen.screen, buttons)

def game_loop(screen, buttons):
    """ Handles game loop until an action is return by a button in the
        buttons sprite renderer.
    """
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BG_COLOR)
    clock = pygame.time.Clock()
    head = Head()
    sprite = pygame.sprite.RenderPlain(head)
    redPdl = pygame.image.load("assets/redPaddle.jpg")
    greenPdl = pygame.image.load("assets/greenPaddle.jpg")

    while True:
        clock.tick(60)

        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            elif event.type == MOUSEBUTTONDOWN:
               head.hit()

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        sprite.update()
        screen.blit(background, (0, 0))
        sprite.draw(screen)
        buttons.draw(screen)
        screen.blit(redPdl, (60, 10))
        screen.blit(greenPdl, (900, 10))

        line_width = 2
        pygame.draw.rect(screen, WHITE, [0,5,SCREEN_WIDTH,line_width]) # top line
        pygame.draw.rect(screen, WHITE, [0,SCREEN_HEIGHT-5,SCREEN_WIDTH,line_width]) # bottom line
        pygame.draw.rect(screen, WHITE, [5,0,line_width, SCREEN_HEIGHT]) # left line
        pygame.draw.rect(screen, WHITE, [SCREEN_WIDTH-5,0,line_width, SCREEN_HEIGHT+line_width]) # right line
        pygame.display.flip()

def show_topScore(scr, player, text="0:21"):
    global best_left_score, best_right_score, left_wins, right_wins
    Left_Name = player.Left_Name
    Right_Name = player.Right_Name
    game_font = pygame.font.Font("freesansbold.ttf", 32)
    scr.screen.fill(BG_COLOR)
    player_text = game_font.render("TOP SCORE FOR "+Left_Name+" : "+str(best_left_score[0])+":"+str(best_left_score[1]), False, WHITE)
    scr.screen.blit(player_text, (300,int(scr.screen_height/2)))
    player_text = game_font.render("TOP SCORE FOR "+Right_Name+" : "+str(best_right_score[0])+":"+str(best_right_score[1]), False, WHITE)
    scr.screen.blit(player_text, (300,int(scr.screen_height/2)+60))

    pygame.display.update()

    time.sleep(2)

    return GameState.TITLE

def help_screen(scr):
    screen = scr.screen
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    help_lt = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2)+30),
        font_size=30,
        bg_rgb=LIGHT_RED,
        text_rgb=WHITE,
        text="LEFT PLAYER CONTROLS : W for Up and S key for Down",
        action=GameState.HELP_LT,
    )
    help_rt = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2)+90),
        font_size=30,
        bg_rgb=LIGHT_GREEN,
        text_rgb=WHITE,
        text="RIGHT PLAYER CONTROLS : UP key for Up and DOWN key for Down",
        action=GameState.HELP_RT,
    )
    back = UIElement(
        center_position=(int(screen_width/2), int(screen_height/2+150)),
        font_size=30,
        bg_rgb=BG_COLOR,
        text_rgb=WHITE,
        text="GO BACK",
        action=GameState.BACK,
    )

    buttons = RenderUpdates(help_lt, help_rt, back)
    return game_loop(screen, buttons)

def main():
    global best_left_score, best_right_score, Left_Name, Right_Name
    pygame.init()
    pygame.display.set_caption('Pong')

    screen = Screen(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)), SCREEN_WIDTH, SCREEN_HEIGHT)
    game_state = GameState.TITLE
    player = Player()

    # read the top score from file and config file
    score = []
    config = []
    for line in open('assets/__score'):
        score.append(tuple(line.strip().split(',')))
    best_left_score[0] = int(score[0][0])
    best_left_score[1] = int(score[0][1])
    best_right_score[0] = int(score[1][0])
    best_right_score[1] = int(score[1][1])

    for line in open('config'):
        config.append(tuple(line.strip().split(':')))
    player.Left_Name = config[0][1]
    player.Right_Name = config[1][1]

    while True:
        if game_state == GameState.BACK:
            game_state = title_screen(screen)

        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.ONE_PLAYER:
            player.two_player = False
            game_state = play_pong(screen, player, game_state)

        if game_state == GameState.TWO_PLAYER:
            player.two_player = True
            game_state = play_pong(screen, player, game_state)

        if game_state == GameState.TOPSCORE:
            game_state = show_topScore(screen, player)

        if game_state == GameState.HELP_LT or game_state == GameState.HELP_RT:
            doNothing = 1
            game_state = GameState.TITLE

        if game_state == GameState.HELP:
            game_state = help_screen(screen)
            game_state = GameState.TITLE

        if game_state == GameState.QUIT:
            pygame.quit()
            return

if __name__ == "__main__":
    main()
