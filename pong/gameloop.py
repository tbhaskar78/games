# Author: Bhaskar Tallamraju
# Date  : 24 Sep 2020

#!/usr/bin/env python3
from common import *

os.putenv('SDL_AUDIODRIVER', 'alsa')
os.putenv('SDL_AUDIODEV', '/dev/audio')

def reset(playerParam, gameParam):
    gameParam.level = 1
    gameParam.right_wins = 0
    gameParam.left_wins = 0
    gameParam.len_of_paddle = LENGTH_OF_PADDLE
    playerParam.rightPlayer_score = 0
    playerParam.leftPlayer_score = 0
    playerParam.leftPlayer_speed = 0 #PADDLE_SPEED

def levelUp(scr, gameParam):
    screen = scr.screen
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    # change the parameters for level up
    gameParam.len_of_paddle -= 30
    game_font = pygame.font.Font("freesansbold.ttf", 32)

    # display the LEVEL INCREASE
    gameParam.level += 1
    if gameParam.level > GAME_MAX_LEVEL:
        screen.fill(BG_COLOR)
        game_fin = game_font.render("END", False, WHITE)
        screen.blit(game_fin, (int(screen_width/2)-10,int(screen_height/2)))
        pygame.display.flip()
        time.sleep(4)
        return
    else:
        screen.fill(BG_COLOR)
        game_level = game_font.render("MAKING IT HARDER NOW"+\
                                      ", DECREASING PADDLE LENGTH by 30%" , False, WHITE)
        screen.blit(game_level, (80, int(screen_height/2)))
        pygame.display.flip()
        time.sleep(4)
        return


def ball_animate(scr, playerParam, gameParam):
    # fetch screen params
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    screen = scr.screen
    # fetch player params
    leftPlayer = playerParam.leftPlayer
    rightPlayer = playerParam.rightPlayer
    ball = gameParam.ball

    #animate
    ball.x += gameParam.ball_speed_x
    ball.y += gameParam.ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(gameParam.pong_sound)
        gameParam.ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(gameParam.score_sound)
        playerParam.rightPlayer_score += 1
        gameParam.score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(gameParam.score_sound)
        playerParam.leftPlayer_score += 1
        gameParam.score_time = pygame.time.get_ticks()

    # check for collision with rightPlayer or leftPlayer
    if ball.colliderect(rightPlayer) and gameParam.ball_speed_x > 0:
        pygame.mixer.Sound.play(gameParam.pong_sound)
        if abs(ball.right - rightPlayer.left) < 10:
            gameParam.ball_speed_x *= -1
        elif abs(ball.bottom - rightPlayer.top) < 10 and gameParam.ball_speed_y > 0:
            gameParam.ball_speed_x *= -1
        elif abs(ball.top - rightPlayer.bottom) < 10 and gameParam.ball_speed_y < 0:
            gameParam.ball_speed_x *= -1

    if gameParam.ball.colliderect(leftPlayer) and gameParam.ball_speed_x < 0:
        pygame.mixer.Sound.play(gameParam.pong_sound)
        if abs(ball.left - leftPlayer.left) < 10:
            gameParam.ball_speed_x *= -1
        elif abs(ball.bottom - leftPlayer.top) < 10 and gameParam.ball_speed_y > 0:
            gameParam.ball_speed_x *= -1
        elif abs(ball.top - leftPlayer.bottom) < 10 and gameParam.ball_speed_y < 0:
            gameParam.ball_speed_x *= -1

def rightPlayer_animate(scr, playerParam, gameParam):
    # fetch screen params
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    # fetch player params
    rightPlayer = playerParam.rightPlayer
    rightPlayer_speed = playerParam.rightPlayer_speed

    rightPlayer.y += rightPlayer_speed
    if rightPlayer.top <= 0:
        rightPlayer.top = 0
    if rightPlayer.bottom >= screen_height:
        rightPlayer.bottom = screen_height

def leftPlayer_animate(scr, playerParam, gameParam):
    # fetch screen params
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    # fetch player params
    leftPlayer = playerParam.leftPlayer
    leftPlayer_speed = playerParam.leftPlayer_speed
    two_player = playerParam.two_player

    ball = gameParam.ball

    if two_player == True:
        leftPlayer.y += leftPlayer_speed
        if leftPlayer.top <= 0:
            leftPlayer.top = 0
        if leftPlayer.bottom >= screen_height:
            leftPlayer.bottom = screen_height

    elif two_player == False:
        if leftPlayer.top < ball.y:
            leftPlayer.top += leftPlayer_speed
        if leftPlayer.top > ball.y:
            leftPlayer.top -= leftPlayer_speed
        if leftPlayer.top <= 0:
            leftPlayer.top = 0
        if leftPlayer.bottom >= screen_height:
            leftPlayer.bottom = screen_height

def ball_start(scr, playerParam, gameParam):
    # fetch screen params
    screen = scr.screen
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    # fetch player params
    leftPlayer = playerParam.leftPlayer
    leftPlayer_speed = playerParam.leftPlayer_speed

    current_time = pygame.time.get_ticks()
    gameParam.ball.center = (int(screen_width/2), int(screen_height/2))
    game_font = pygame.font.Font("freesansbold.ttf", 32)

    # display a counter before starting the ball
    if current_time - gameParam.score_time < 700:
        three = game_font.render("3", False, WHITE)
        screen.blit(three, (int(screen_width/2) - 10, int(screen_height/2) +20))
    elif 700 < current_time - gameParam.score_time < 1400:
        two = game_font.render("2", False, WHITE)
        screen.blit(two, (int(screen_width/2) - 10, int(screen_height/2) +20))
    elif 1400 < current_time - gameParam.score_time < 2100:
        one = game_font.render("1", False, WHITE)
        screen.blit(one, (int(screen_width/2) - 10, int(screen_height/2) +20))


    if current_time - gameParam.score_time < 2100:
        gameParam.ball_speed_x, gameParam.ball_speed_y = 0, 0
    else:
        gameParam.ball_speed_y = BALL_SPEED*random.choice((1, -1))
        gameParam.ball_speed_x = BALL_SPEED*random.choice((1, -1))
        gameParam.score_time = None

def act_on_score(scr, playerParam, gameParam):
    screen = scr.screen
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    game_font = pygame.font.Font("freesansbold.ttf", 32)


    screen.fill(BG_COLOR)
    playerParam.rightPlayer_score = 0
    playerParam.leftPlayer_score = 0
    time.sleep(2)
    if gameParam.level >= GAME_MAX_LEVEL:
        gameParam.len_of_paddle = LENGTH_OF_PADDLE
        playerParam.leftPlayer_speed = 0 #PADDLE_SPEED
        if gameParam.left_wins > gameParam.right_wins:
            match_win = game_font.render(playerParam.Left_Name+"  WINS THE MATCH "\
                                           +str(gameParam.left_wins)+" - "\
                                           +str(gameParam.right_wins), False, WHITE)
        else:
            match_win = game_font.render(playerParam.Right_Name+"  WINS THE MATCH "\
                                           +str(gameParam.right_wins)+" - "+\
                                           str(gameParam.left_wins), False, WHITE)
        screen.blit(match_win, (int(screen_width/4),int(screen_height/2)))
        pygame.display.flip()
        time.sleep(4)
        gameParam.left_wins = 0
        gameParam.right_wins = 0
        return GameState.TITLE

def play_pong(scr, playerParam, gameParam, game_state):
    # fetch screen params
    screen_width = scr.screen_width
    screen_height = scr.screen_height
    screen = scr.screen

    # fetch game params
    len_of_paddle = gameParam.len_of_paddle

    # fetch player params
    Left_Name = playerParam.Left_Name
    Right_Name = playerParam.Right_Name
    if playerParam.two_player == False:
        playerParam.leftPlayer_speed = PADDLE_SPEED

    # draw the paddles for both rightPlayers
    playerParam.rightPlayer = pygame.Rect(screen_width-20, int(screen_height/2)-70, 10, len_of_paddle)
    playerParam.leftPlayer = pygame.Rect(10, int(screen_height/2)-70, 10, len_of_paddle)
    clock = pygame.time.Clock()
    game_font = pygame.font.Font("freesansbold.ttf", 32)

    # draw the ball
    gameParam.ball = pygame.Rect(int(screen_width/2)-15, int(screen_height/2)-15, 20, 20)
    # sound
    gameParam.pong_sound = pygame.mixer.Sound("assets/pong.ogg")
    gameParam.score_sound = pygame.mixer.Sound("assets/score.ogg")
    gameParam.score_time = pygame.time.get_ticks()

    # Show level info
    screen.fill(BG_COLOR)
    game_level = game_font.render("GAME NUMBER "+str(gameParam.level)+\
                                  "/"+str(GAME_MAX_LEVEL)+\
                                  " BETWEEN "+str(playerParam.Left_Name)+\
                                  " & "+str(playerParam.Right_Name), False, WHITE)
    screen.blit(game_level, (int(screen_width/4)-150, int(screen_height/2)))
    pygame.display.flip()
    time.sleep(4)


    # LOOP forever
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
                reset(playerParam, gameParam)
                return GameState.TITLE
            # control rightPlayer paddle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    playerParam.rightPlayer_speed += PADDLE_SPEED
                if event.key == pygame.K_UP:
                    playerParam.rightPlayer_speed -= PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    playerParam.rightPlayer_speed -= PADDLE_SPEED
                if event.key == pygame.K_UP:
                    playerParam.rightPlayer_speed += PADDLE_SPEED
            # control leftPlayer paddle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    playerParam.leftPlayer_speed += PADDLE_SPEED
                if event.key == pygame.K_w:
                    playerParam.leftPlayer_speed -= PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    playerParam.leftPlayer_speed -= PADDLE_SPEED
                if event.key == pygame.K_w:
                    playerParam.leftPlayer_speed += PADDLE_SPEED

        if playerParam.leftPlayer_score >= GAME_SCORE:
            if gameParam.best_left_score[0] < playerParam.leftPlayer_score:
                gameParam.best_left_score[0] = playerParam.leftPlayer_score
                gameParam.best_left_score[1] = playerParam.rightPlayer_score
                # update the score
                filename = "assets/__score."+playerParam.Right_Name
                with open(filename, 'w') as f:
                    f.write(str(playerParam.leftPlayer_score)+","+\
                            str(playerParam.rightPlayer_score)+","+\
                            str(gameParam.level))
            gameParam.left_wins += 1
            screen.fill(BG_COLOR)
            if gameParam.level < GAME_MAX_LEVEL:
                player_text = game_font.render(playerParam.Left_Name+"  WINS!", False, WHITE)
                screen.blit(player_text, (int(screen_width/2)-150, int(screen_height/2)))
                pygame.display.flip()
            state = act_on_score(scr, playerParam, gameParam)
            if gameParam.level >= GAME_MAX_LEVEL:
                gameParam.level = 1
                return state
            # check if one rightPlayer, then exit the match
            #if playerParam.two_player == False:
            #    return GameState.TITLE
            levelUp(scr, gameParam)
            return game_state

        elif playerParam.rightPlayer_score >= GAME_SCORE:
            if gameParam.best_right_score[0] < playerParam.rightPlayer_score:
                gameParam.best_right_score[0] = playerParam.rightPlayer_score
                gameParam.best_right_score[1] = playerParam.leftPlayer_score
                # update the score
                filename = "assets/__score."+playerParam.Right_Name
                with open(filename, 'w') as f:
                    f.write(str(playerParam.rightPlayer_score)+","+\
                            str(playerParam.leftPlayer_score)+","+\
                            str(gameParam.level))
            gameParam.right_wins += 1
            screen.fill(BG_COLOR)
            if gameParam.level < GAME_MAX_LEVEL:
                player_text = game_font.render(playerParam.Right_Name+"  WINS!", False, WHITE)
                screen.blit(player_text, (int(screen_width/2)-150, int(screen_height/2)))
                pygame.display.flip()
            state = act_on_score(scr, playerParam, gameParam)
            if gameParam.level >= GAME_MAX_LEVEL:
                gameParam.level = 1
                return state
            levelUp(scr, gameParam)
            return game_state
        else:
            ball_animate(scr, playerParam, gameParam)
            rightPlayer_animate(scr, playerParam, gameParam)
            leftPlayer_animate(scr, playerParam, gameParam)

        # visuals
        screen.fill(BG_COLOR)
        #pygame.draw.rect
        rect(screen, LIGHT_GREEN, playerParam.rightPlayer)
        #pygame.draw.rect
        rect(screen, LIGHT_RED, playerParam.leftPlayer)
        pygame.draw.ellipse(screen, pygame.Color('orange'), gameParam.ball)
        pygame.draw.aaline(screen, LIGHT_GREY, (screen_width/2, 0), (screen_width/2, screen_height))

        # should always get called
        if gameParam.score_time:
            ball_start(scr, playerParam, gameParam)

        rightPlayer_text = game_font.render(f"{playerParam.rightPlayer_score}", False, LIGHT_GREEN)
        screen.blit(rightPlayer_text, (int(screen_width/2)+int(screen_width/4),0+8))

        leftPlayer_text = game_font.render(f"{playerParam.leftPlayer_score}", False, WHITE)
        screen.blit(leftPlayer_text, (int(screen_width/4)-16,0+8))

        line_width = 2
        pygame.draw.rect(screen, WHITE, [0,5,SCREEN_WIDTH,line_width]) # top line
        pygame.draw.rect(screen, WHITE, [0,SCREEN_HEIGHT-5,SCREEN_WIDTH,line_width]) # bottom line
        pygame.draw.rect(screen, WHITE, [5,0,line_width, SCREEN_HEIGHT]) # left line
        pygame.draw.rect(screen, WHITE, [SCREEN_WIDTH-5,0,line_width, SCREEN_HEIGHT+line_width]) # right line

        pygame.display.flip()
        clock.tick(60)

def main():
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
