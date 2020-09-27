#!/usr/bin/python3

# Author: Bhaskar Tallamraju
# Date  : 24 Sep 2020
from gameloop import *
from common import *
from os import path

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

def show_topScore(scr, player, gameParam):
    Left_Name = player.Left_Name
    Right_Name = player.Right_Name
    game_font = pygame.font.Font("freesansbold.ttf", 32)
    scr.screen.fill(BG_COLOR)
    player_text = game_font.render("TOP SCORE FOR "+Left_Name+\
                                   " : "+str(gameParam.best_left_score[0])+\
                                   ":"+str(gameParam.best_left_score[1])+\
                                   " AT LEVEL "+str(gameParam.best_left_level), False, WHITE)
    scr.screen.blit(player_text, (300,int(scr.screen_height/2)))
    player_text = game_font.render("TOP SCORE FOR "+Right_Name+" : "+\
                                   str(gameParam.best_right_score[0])+\
                                   ":"+str(gameParam.best_right_score[1])+\
                                   " AT LEVEL "+str(gameParam.best_right_level), False, WHITE)

    scr.screen.blit(player_text, (300,int(scr.screen_height/2)+60))

    pygame.display.update()

    time.sleep(4)

    return GameState.TITLE

def help_screen(scr):
    screen = scr.screen
    screen_width = scr.screen_width
    screen_height = scr.screen_height

    game_font = pygame.font.Font("freesansbold.ttf", 32)
    scr.screen.fill(BG_COLOR)
    text0=B"INSTRUCTIONS: BEST OF 3 GAMES, WITH INCREASING DIFFICULTY"
    help_rt = game_font.render(text0, False, WHITE)
    scr.screen.blit(help_rt, (50,int(scr.screen_height/2)-60))
    text1=B"* RIGHT PLAYER CONTROLS : UP key for Up and DOWN key for Down"
    help_rt = game_font.render(text1, False, LIGHT_GREEN)
    scr.screen.blit(help_rt, (50,int(scr.screen_height/2)))
    text2=B"* LEFT PLAYER CONTROLS : W key for Up and S key for Down"
    help_lt = game_font.render(text2, False, LIGHT_RED)
    scr.screen.blit(help_lt, (50,int(scr.screen_height/2)+60))
    text3=B"<< RETURN TO TITLE SCREEN"
    help_lt = game_font.render(text3, False, WHITE)
    scr.screen.blit(help_lt, (50,int(scr.screen_height/2)+120))
    pygame.display.update()

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == MOUSEBUTTONDOWN:
                return

def main():
    pygame.mixer.pre_init(44100, -16, 2, 128)
    pygame.init()
    pygame.display.set_caption('Pong')
    game_sound = pygame.mixer.Sound("assets/hero.ogg")

    screen = Screen(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)), SCREEN_WIDTH, SCREEN_HEIGHT)
    game_state = GameState.TITLE
    player = Player()
    gameParam = GameParams()

    # read the top score from file and config file
    score_lt = []
    score_rt = []
    config = []

    for line in open('config'):
        config.append(tuple(line.strip().split(':')))
    player.Left_Name = config[0][1]
    player.Right_Name = config[1][1]

    filename = "assets/__score."+player.Left_Name
    if path.exists(filename):
        with open(filename) as f:
            Lines = f.readlines()
            for line in Lines:
                score_lt.append(tuple(line.strip().split(',')))
                gameParam.best_left_score[0] = (score_lt[0][0])
                gameParam.best_left_score[1] = (score_lt[0][1])
                gameParam.best_left_level = score_lt[0][2]

    filename = "assets/__score."+player.Right_Name
    if path.exists(filename):
        with open(filename) as f:
            Lines = f.readlines()
            for line in Lines:
                score_rt.append(tuple(line.strip().split(',')))
                gameParam.best_right_score[0] = (score_rt[0][0])
                gameParam.best_right_score[1] = (score_rt[0][1])
                gameParam.best_right_level = score_rt[0][2]

    pygame.mixer.Sound.play(game_sound)
    while True:
        if game_state == GameState.BACK:
            game_state = title_screen(screen)

        if game_state == GameState.TITLE:
            pygame.mixer.Sound(game_sound).play(-1)
            game_state = title_screen(screen)

        if game_state == GameState.ONE_PLAYER:
            player.two_player = False
            pygame.mixer.stop()
            game_state = play_pong(screen, player, gameParam, game_state)
            pygame.mixer.stop()

        if game_state == GameState.TWO_PLAYER:
            player.two_player = True
            pygame.mixer.stop()
            game_state = play_pong(screen, player, gameParam, game_state)
            pygame.mixer.stop()

        if game_state == GameState.TOPSCORE:
            game_state = show_topScore(screen, player, gameParam)

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
