# Author: Bhaskar Tallamraju
# Date  : 24 Sep 2020

#!/usr/bin/env python3
from common import *

os.putenv('SDL_AUDIODRIVER', 'alsa')
os.putenv('SDL_AUDIODEV', '/dev/audio')

# setting up the main window
len_of_paddle = 100
player_speed = 0
opponent_speed = 0 #PADDLE_SPEED
ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))

# score
player_score = 0
opponent_score = 0
score_time = True
ball = None
player = None
opponent = None
pong_sound = None
score_sound = None
level = 1

def levelUp(scr):
    global level, len_of_paddle, game_font
    screen = scr.screen
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    # change the parameters for level up
    len_of_paddle -= 30

    # display the LEVEL INCREASE
    level += 1
    if level > 3:
        screen.fill(BG_COLOR)
        game_fin = game_font.render("END", False, WHITE)
        screen.blit(game_fin, (int(screen_width/2)-10,int(screen_height/2)))
        pygame.display.flip()
        time.sleep(4)
        return
    else:
        screen.fill(BG_COLOR)
        game_fin = game_font.render("LEVEL INCREASED TO : "+str(level), False, WHITE)
        screen.blit(game_fin, (int(screen_width/2)-150,int(screen_height/2)))
        pygame.display.flip()
        time.sleep(4)
        return


def ball_animate(screen_width, screen_height):
    global ball, ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, pong_sound, score_sound
    #animate
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    # check for collision with player or opponent
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_x *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_x *= -1

def player_animate(screen_width, screen_height):
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animate(two_player,screen_width, screen_height):
    if two_player == True:
        opponent.y += opponent_speed
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= screen_height:
            opponent.bottom = screen_height

    elif two_player == False:
        if opponent.top < ball.y:
            opponent.top += opponent_speed
        if opponent.top > ball.y:
            opponent.top -= opponent_speed
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= screen_height:
            opponent.bottom = screen_height

def ball_start(screen, screen_width, screen_height):
    global score_time, ball, ball_speed_x, ball_speed_y, game_font
    current_time = pygame.time.get_ticks()
    ball.center = (int(screen_width/2), int(screen_height/2))

    # display a counter before starting the ball
    if current_time - score_time < 700:
        three = game_font.render("3", False, WHITE)
        screen.blit(three, (int(screen_width/2) - 10, int(screen_height/2) +20))
    elif 700 < current_time - score_time < 1400:
        two = game_font.render("2", False, WHITE)
        screen.blit(two, (int(screen_width/2) - 10, int(screen_height/2) +20))
    elif 1400 < current_time - score_time < 2100:
        one = game_font.render("1", False, WHITE)
        screen.blit(one, (int(screen_width/2) - 10, int(screen_height/2) +20))


    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = BALL_SPEED*random.choice((1, -1))
        ball_speed_x = BALL_SPEED*random.choice((1, -1))
        score_time = None


def play_pong(scr, playerParam, game_state):
    global ball, player, opponent, player_speed, opponent_speed, score_time, game_font, pong_sound, score_sound
    global level, opponent_score, player_score, len_of_paddle
    global best_left_score, best_right_score, left_wins, right_wins

    # fetch screen params
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    screen = scr.screen

    if playerParam.two_player == False:
        opponent_speed = PADDLE_SPEED

    Left_Name = playerParam.Left_Name
    Right_Name = playerParam.Right_Name

    # draw the ball
    ball = pygame.Rect(int(screen_width/2)-15, int(screen_height/2)-15, 20, 20)
    # draw the paddles for both players
    player = pygame.Rect(screen_width-20, int(screen_height/2)-70, 10, len_of_paddle)
    opponent = pygame.Rect(10, int(screen_height/2)-70, 10, len_of_paddle)
    clock = pygame.time.Clock()
    game_font = pygame.font.Font("freesansbold.ttf", 32)
    # sound
    pong_sound = pygame.mixer.Sound("assets/pong.ogg")
    score_sound = pygame.mixer.Sound("assets/score.ogg")
    score_time = pygame.time.get_ticks()

    # LOOP forever
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # control player paddle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player_speed -= PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player_speed += PADDLE_SPEED

            # control opponent paddle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    opponent_speed += PADDLE_SPEED
                if event.key == pygame.K_w:
                    opponent_speed -= PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    opponent_speed -= PADDLE_SPEED
                if event.key == pygame.K_w:
                    opponent_speed += PADDLE_SPEED

        if opponent_score >= GAME_SCORE:
            if best_left_score[0] < opponent_score:
                best_left_score[0] = opponent_score
                best_left_score[1] = player_score
            left_wins += 1
            screen.fill(BG_COLOR)
            if level < 3:
                player_text = game_font.render(Left_Name+"  WINS!", False, WHITE)
                screen.blit(player_text, (int(screen_width/2)-150, int(screen_height/2)))
                pygame.display.flip()
            player_score = 0
            opponent_score = 0
            time.sleep(2)
            if level >= 3:
                level = 1
                len_of_paddle = 100
                opponent_speed = 0 #PADDLE_SPEED
                if left_wins > right_wins:
                    player_text = game_font.render(Left_Name+"  WINS THE MATCH "+str(left_wins)+" - "+str(right_wins), False, WHITE)
                else:
                    player_text = game_font.render(Right_Name+"  WINS THE MATCH "+str(right_wins)+" - "+str(left_wins), False, WHITE)
                screen.blit(player_text, (int(screen_width/4),int(screen_height/2)))
                pygame.display.flip()
                time.sleep(4)
                left_wins = 0
                right_wins = 0
                return GameState.TITLE
            if playerParam.two_player == False:
                return GameState.TITLE
            levelUp(scr)
            #pygame.quit()
            return game_state

        elif player_score >= GAME_SCORE:
            if best_right_score[1] < player_score:
                best_right_score[0] = opponent_score
                best_right_score[1] = player_score
            right_wins += 1
            screen.fill(BG_COLOR)
            if level < 3:
                player_text = game_font.render(Right_Name+"  WINS!", False, WHITE)
                screen.blit(player_text, (int(screen_width/2)-150,int(screen_height/2)))
                pygame.display.flip()
            player_score = 0
            opponent_score = 0
            time.sleep(2)
            if level >= 3:
                level = 1
                len_of_paddle = 100
                opponent_speed = 0 #PADDLE_SPEED
                if left_wins > right_wins:
                    player_text = game_font.render(Left_Name+"  WINS THE MATCH "+str(left_wins)+" - "+str(right_wins), False, WHITE)
                else:
                    player_text = game_font.render(Right_Name+"  WINS THE MATCH "+str(right_wins)+" - "+str(left_wins), False, WHITE)
                screen.blit(player_text, (int(screen_width/4),int(screen_height/2)))
                pygame.display.flip()
                time.sleep(4)
                left_wins = 0
                right_wins = 0
                return GameState.TITLE
            #pygame.quit()
            levelUp(scr)
            return game_state
        else:
            ball_animate(screen_width, screen_height)
            player_animate(screen_width, screen_height)
            opponent_animate(playerParam.two_player, screen_width, screen_height)

        # visuals
        screen.fill(BG_COLOR)
        #pygame.draw.rect
        rect(screen, LIGHT_GREEN, player)
        #pygame.draw.rect
        rect(screen, LIGHT_RED, opponent)
        pygame.draw.ellipse(screen, pygame.Color('orange'), ball)
        pygame.draw.aaline(screen, LIGHT_GREY, (screen_width/2, 0), (screen_width/2, screen_height))

        # should always get called
        if score_time:
            ball_start(screen, screen_width, screen_height)

        player_text = game_font.render(f"{player_score}", False, LIGHT_GREEN)
        screen.blit(player_text, (int(screen_width/2)+int(screen_width/4),0+8))

        opponent_text = game_font.render(f"{opponent_score}", False, WHITE)
        screen.blit(opponent_text, (int(screen_width/4)-16,0+8))

        line_width = 2
        pygame.draw.rect(screen, WHITE, [0,5,SCREEN_WIDTH,line_width]) # top line
        pygame.draw.rect(screen, WHITE, [0,SCREEN_HEIGHT-5,SCREEN_WIDTH,line_width]) # bottom line
        pygame.draw.rect(screen, WHITE, [5,0,line_width, SCREEN_HEIGHT]) # left line
        pygame.draw.rect(screen, WHITE, [SCREEN_WIDTH-5,0,line_width, SCREEN_HEIGHT+line_width]) # right line

        pygame.display.flip()
        clock.tick(60)

def play_level(screen, player):
    return_main = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    buttons = RenderUpdates(return_main)

    return game_loop(screen.screen, buttons)

def main():
    global score_time
    # SETUP
    pygame.mixer.pre_init(44100, -16, 2, 128)
    pygame.init()

    screen = Screen(pygame.display.set_mode((1200, 650)))
    pygame.display.set_caption('Pong')
    rtn_button = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )
    buttons = RenderUpdates(rtn_button)

    play_pong(screen, player)

if __name__ == "__main__":
    main()
