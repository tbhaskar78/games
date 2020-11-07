#! /usr/bin/python3

from assets.gamelib.gamelib import *
import os
import random
from assets.gamelib.cut_scenes import *


level = [
       # LEVEL 1
       ["GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "G      H              L        E           G",
        "G    W                                W    G",
        "G                                     F    G",
        "G  C   PPP             PPPPPPPPPP          G",
        "G                  PPPP                    G",
        "GP               PP                        G",
        "G                            W       PPPP  G",
        "G      PPPPP                               G",
        "G    PP    PPPP                            G",
        "G                          GGGGGG          G",
        "GP                PPPPPP                   G",
        "G                                          G",
        "G      G                              C   KG",
        "GPP    GPP                    PPPPPP       G",
        "G                                          G",
        "G   d        d                           PPG",
        "G   PPPPPPPPPPPP                      P    G",
        "G                                  P       G",
        "G    W                 PP  PP         W    G",
        "e    F          PPP                   F    G",
        "   C    S                      PP  S       G",
        "GG                                    f    G",
        "GGGG                    d         d        G",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",],

       # LEVEL 2
       ["GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "G          u  H      L                     G",
        "GE                                         G",
        "G    W       PP                       W    G",
        "G         PPP                  GG     F  PPG",
        "GPPPP                        PPGG          G",
        "G                PP            GG          G",
        "G     GG             PPPPP     GGPPP       G",
        "G     GG             GG        GG          G",
        "G     GGd           PGG        GG       C  G",
        "G     PPPPPP         GG        GG          G",
        "G          PPPP      GG        GG          G",
        "G                  PPGG    PPPPPP  PPPPPPPPG",
        "GPPP     W                                 G",
        "G    C       C          d                  G",
        "G               PPPPPPPPP                  G",
        "G                 GG                       G",
        "G      P          GG                     K G",
        "G      PPPPP      GG          PPPP         G",
        "G                 GG             PP        G",
        "e    W            GG                  W PPPG",
        "        C     PPPPGG              S        G",
        "GG                                     f   G",
        "GGGG                                       G",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",],

       # LEVEL 3
       ["GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "G          u         L                D    G",
        "G                                          G",
        "G    W                            C   W  C G",
        "G                             PGGP    F    G",
        "G                              GG          G",
        "G                   PPP        GG          G",
        "G                    GGP       GGPPP       G",
        "G             PP     GG        GG        E G",
        "G    d   d           GG      PPGG          G",
        "G  PPPPPPPP         PGG     P  GG          G",
        "G       D            GG        GG       PPPG",
        "GP                   GG                    G",
        "G  H  C  W    P   PGPGGPGP                 G",
        "G            P       GG PPP                G",
        "G  PP                GG D                  G",
        "G                    GG        PPPP         G",
        "G        PPPP        GG                    G",
        "G            P       GG                    G",
        "G                    GGPPP   P             G",
        "e    W             PPGG       P       W    G",
        "        C        PP  GG  K      P S        G",
        "GG                   GG                f   G",
        "GGGG      GG         GG    d               G",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",],

       # LEVEL 4
       ["GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "G   D      u         L                D    G",
        "G                                          G",
        "G  CWC                              C W C  G",
        "G H K   G    P                PGGP    F    G",
        "G       G                      GG          G",
        "G       GP              PPP    GG          G",
        "GGGGGGGGG                      GGPP      PPG",
        "G       GGP                    GG          G",
        "G            PP              PPGG        E G",
        "G                              GG  P       G",
        "G                         d    GG          G",
        "G      PP  PP  PPPPPP     PPPPP  PP     PPPG",
        "GP            W                      W     G",
        "G                                          G",
        "G                                          G",
        "GPPP     PP  PPP    PP   P     PP  P  P    G",
        "G    P                                    PG",
        "G                                          G",
        "G                d               d         G",
        "e         GGGGGGGGGGPPPP     PPGGGGPPPP    G",
        "            C   W   C             S       PG",
        "GG                                         G",
        "GGGG                      d                G",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",],

       # LEVEL 5
       ["GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "G       u  H         L        uu        K  G",
        "G                                          G",
        "G C  W  C      PP           C  W  C   d   dG",
        "GPP       PPP       PP                PPPPPG",
        "G                                    P     G",
        "G  PP                    PP        PP      G",
        "G      PP                                  G",
        "G           PP                 PP          G",
        "G                                          G",
        "GPP              P         PP              G",
        "G                                          G",
        "G                      PPPd                G",
        "GPPPPP  PP   P                   C  W  C   G",
        "G                   PP                     G",
        "G                                          G",
        "G C  W  C        PP                        G",
        "G                                          G",
        "G            PP                            G",
        "G                                          G",
        "e        P                                 G",
        "        P   C   W   C             S    E   G",
        "GG                                         G",
        "GGGG                      d                G",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",],]

def gameRoomBuild(screen, entities, platforms, levelIndex):
    global level
    global MULTIPLIER

    x = y = 0
    # build the level
    for row in level[levelIndex]:
        for col in row:
            if col == "u":
                #p = Platform(x, y, "assets/img/upNails.png", 50, 40)
                sp = SpearBlock(x, y, screen, "assets/img/upNails.png")
                platforms.append(sp)
                entities.add(sp)
            if col == "d":
                #p = Platform(x, y+10, "assets/img/downNail.png", 50, 40)
                sp = SpearBlock(x, y+10, screen, "assets/img/downNail.png")
                platforms.append(sp)
                entities.add(sp)
            if col == "e":
                p = Platform(x, y, "assets/img/entryDoor.png", 40, 100)
                platforms.append(p)
                entities.add(p)
            if col == "f":
                p = Platform(x, y, "assets/img/fireplace.png", 100, 100)
                entities.add(p)
            if col == "F":
                p = Platform(x, y, "assets/img/flag_red.png", 100, 100)
                entities.add(p)
            if col == "W":
                p = Platform(x, y, "assets/img/window.png", 100, 140)
                entities.add(p)
            if col == "L":
                p = Platform(x, y, "assets/img/chandelier.png", 100, 140)
                entities.add(p)
            if col == "C":
                p = Platform(x, y, "assets/img/candle.png")
                entities.add(p)
            if col == "P":
                p = Platform(x, y, "assets/img/woodplanks.jpg")
                platforms.append(p)
                entities.add(p)
            if col == "G":
                p = Platform(x, y, "assets/img/platform-top.png") #gray1.png")
                platforms.append(p)
                entities.add(p)
            if col == "S":
                p = Platform(x, y, "assets/img/statue.png", 100, 140)
                entities.add(p)
            if col == "E":
                exitObject = ExitBlock(x, y+5, screen, "assets/img/door_0.png")
                platforms.append(exitObject)
                entities.add(exitObject)
            if col == "K":
                keyObject = KeyBlock(x, y, screen)
                platforms.append(keyObject)
                entities.add(keyObject)
            if col == "H": # food/Health
                foodObject = Food(x, y, screen)
                platforms.append(foodObject)
                entities.add(foodObject)
            x += MULTIPLIER
        y += MULTIPLIER
        x = 0
    return entities, platforms, keyObject, exitObject, foodObject

def buildEntities(screen, platforms, entities, enemygroup, levelIndex,
                  maxLivesLeft, score):
    global MULTIPLIER
    # build the enemies
    if True:
        enemygroup.add(Goomba(MULTIPLIER*6, MULTIPLIER*23, screen))
        enemygroup.add(Goomba(MULTIPLIER*9, MULTIPLIER*14, screen))
        enemygroup.add(Goomba(MULTIPLIER*7, MULTIPLIER*4, screen))
        enemygroup.add(Goomba(MULTIPLIER*11, MULTIPLIER*10, screen))
        enemygroup.add(Goomba(MULTIPLIER*17, MULTIPLIER*9, screen))

        enemygroup.add(Bubble(MULTIPLIER*19, MULTIPLIER*12, screen))
        enemygroup.add(Bubble(MULTIPLIER*25, MULTIPLIER*3, screen))
        enemygroup.add(Bubble(MULTIPLIER*29, MULTIPLIER*18, screen))
        enemygroup.add(Bubble(MULTIPLIER*13, MULTIPLIER*11, screen))
        enemygroup.add(Bubble(MULTIPLIER*32, MULTIPLIER*9, screen))

    # build the level with player
    player = Player(MULTIPLIER*2, MULTIPLIER*22, maxLivesLeft, screen, score)
    entities, platforms, keyObject, exitObject, foodObject = gameRoomBuild(screen, entities, platforms, levelIndex)

    total_level_width  = len(level[levelIndex][0])*MULTIPLIER
    total_level_height = len(level[levelIndex])*MULTIPLIER
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    return platforms, entities, enemygroup, camera, player, keyObject, exitObject, foodObject

def main():
    global MULTIPLIER
    global level
    global DEBUG

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    score = 0
    exitObject = None
    keyObject = None
    nextLevel = True
    levelIndex = 0
    currentLevel = 0
    health = 9
    maxLives = 3
    pygame.mixer.pre_init(44100, -16, 2, 128)
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Castle Raider")
    timer = pygame.time.Clock()
    #Create Display
    displayHeart = Display("assets/img/heart.png", screen, health, (WIN_WIDTH-150), (16, 16))
    displayFace = Display("assets/img/face.png", screen, maxLives, 30, (25, 25), 30)

    up = down = left = right = running = False
    if True:
        bg = Surface((WIN_WIDTH, WIN_HEIGHT)).convert()
        bg.fill((0,0,0))
    else:
        bg = pygame.image.load('assets/img/bg_gray3.jpg').convert()
        bg = pygame.transform.scale(bg, (screen.get_width(),
                                         screen.get_height()))

    platforms = []
    entities = pygame.sprite.Group()
    enemygroup = pygame.sprite.Group()

    pygame.mixer.music.load('assets/ogg/maintheme.ogg')
    pygame.mixer.music.play(-1)
    title_scene(screen)
    pygame.mixer.music.stop()

    while 1:
        timer.tick(60)

        if nextLevel == True:
            nextLevel = False
            # play the mario theme forever
            pygame.mixer.music.load('assets/ogg/maintheme.ogg')
            pygame.mixer.music.play(-1)

            if (levelIndex) == len(level):
                pygame.event.post(pygame.event.Event(QUIT))
            else:
                platforms.clear()
                entities.empty()
                enemygroup.empty()

                platforms, entities, enemygroup, camera, player, keyObject, exitObject, foodObject  = buildEntities(screen,
                                                                                                                    platforms,
                                                                                                                    entities,
                                                                                                                    enemygroup,
                                                                                                                    levelIndex,
                                                                                                                    maxLives,
                                                                                                                    score)
                pygame.event.clear()
                currentLevel = levelIndex

                if currentLevel == 0:
                    # Create a cut scene first
                    walk1= pygame.image.load('assets/img/adventBoy_stand1.png')
                    walk1 = pygame.transform.scale(walk1, (MULTIPLIER*2, 32*5))
                    walk1.set_colorkey((0, 0, 0))
                    walk2= pygame.image.load('assets/img/adventBoy_stand2.png')
                    walk2 = pygame.transform.scale(walk2, (MULTIPLIER*2, 32*5))
                    pp_sad1= pygame.image.load('assets/img/pp_sad1.png')
                    pp_sad1 = pygame.transform.scale(pp_sad1, (MULTIPLIER*2, 32*5))
                    pp_sad2= pygame.image.load('assets/img/pp_sad2.png')
                    pp_sad2 = pygame.transform.scale(pp_sad2, (MULTIPLIER*2, 32*5))
                    pp_sad3= pygame.image.load('assets/img/pp_sad3.png')
                    pp_sad3 = pygame.transform.scale(pp_sad3, (MULTIPLIER*2, 32*5))

                    #Copyright attribution: Skeleton sprite used in intro is from artwork done by Irina Mir (irmirx)
                    guard =  pygame.image.load("assets/img/guard1.png")
                    guard = pygame.transform.scale(guard, (MULTIPLIER*3, 32*5))

                    walk = [walk1, walk2]
                    pp_sad= [pp_sad1, pp_sad2, pp_sad3]
                    cut_scene_manager = CutSceneManager(player, screen)
                    cut_scene_manager.update(bg, walk, pp_sad, guard)
                    del cut_scene_manager

                drawCurtains(screen, (levelIndex+1))

                levelIndex += 1

        elif nextLevel == False: # do not update anything if nextLevel is set to True
            # Process events
            for e in pygame.event.get():
                if e.type == ONE_UP:
                    try:
                        entities.remove(foodObject)
                        platforms.remove(foodObject)
                        del foodObject
                    except:
                        print("foodObject could not be removed")

                elif e.type == REDRAW_DOOR:
                    try:
                        entities.remove(keyObject)
                        platforms.remove(keyObject)
                    except:
                        print("KeyObject could not be removed")

                    x, y, dimx, dimy = exitObject.getDimensions()
                    platforms.remove(exitObject)
                    entities.remove(exitObject)
                    exitObject = ExitBlock(x, y, screen, "assets/img/door_1.png")
                    platforms.append(exitObject)
                    entities.add(exitObject)

                elif e.type == NEXT_LEVEL:
                    nextLevel = True
                    up = False
                    down = False
                    right = False
                    left = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound('assets/ogg/goal.ogg').play()
                    time.sleep(8.0)
                    break

                elif e.type == DEAD:
                    #pygame.display.update()
                    if DEBUG == True:
                        print ("Player Dead!")
                    up = False
                    down = False
                    right = False
                    left = False
                    pygame.mixer.music.stop()
                    time.sleep(0.1)
                    pygame.mixer.Sound('assets/ogg/death.ogg').play()
                    time.sleep(4.0)
                    levelIndex = currentLevel
                    pygame.event.clear()
                    maxLives -= 1
                    if maxLives > 0:
                        nextLevel = True
                        platforms.clear()
                        entities.empty()
                        enemygroup.empty()
                        break
                    else:
                        if DEBUG == True:
                            print("etype is DEAD, EXITING")
                        drawCurtains(screen, 0, "Princess Ella is lost forever !")
                        raise SystemExit("DEAD")

                elif e.type == QUIT:
                    pygame.mixer.music.stop()
                    time.sleep(0.1)
                    pygame.mixer.Sound('assets/ogg/death.ogg').play()
                    drawCurtains(screen, 0, "Princess Ella is lost forever !")
                    raise SystemExit("EXITING")

                elif e.type == HURT:
                    pygame.display.update()
                    if DEBUG == True:
                        print ("Player hurt and Dead!")
                    #health, maxLives = player.getPlayerHealth()
                    pygame.mixer.Sound('assets/ogg/ouch.ogg').play()
                    up = False
                    down = False
                    right = False
                    left = False
                    if health <= 0:
                        if DEBUG == True:
                            print ("Health is Zero, Player hurt and Dead!")
                        pygame.event.clear()
                        levelIndex = currentLevel
                        maxLives -= 1
                        if maxLives > 0:
                            nextLevel = True
                            platforms.clear()
                            entities.empty()
                            enemygroup.empty()
                            break
                        else:
                            pygame.mixer.music.stop()
                            time.sleep(0.1)
                            pygame.mixer.Sound('assets/ogg/death.ogg').play()
                            drawCurtains(screen, 0, "Princess Ella is lost forever !")
                            raise SystemExit("DEAD")

                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    print ("Hope you enjoyed the Castle Raider !")
                    pygame.mixer.music.stop()
                    time.sleep(0.1)
                    pygame.mixer.Sound('assets/ogg/death.ogg').play()
                    drawCurtains(screen, 0, "Princess Ella is lost forever !")
                    raise SystemExit("ESCAPE")

                elif e.type == KEYDOWN:
                    if  e.key == K_UP:
                        up = True
                    elif e.key == K_DOWN:
                        down = True
                    elif e.key == K_LEFT:
                        left = True
                    elif e.key == K_RIGHT:
                        right = True
                    elif e.key == K_SPACE:
                        running = True

                elif e.type == KEYUP:
                    if e.key == K_UP:
                        up = False
                    elif e.key == K_DOWN:
                        down = False
                    elif e.key == K_RIGHT:
                        right = False
                    elif e.key == K_LEFT:
                        left = False


            screen.blit(bg,(0,0))
            camera.update(player)

            # update player, draw everything else
            if player.update(up, down, left, right, running, platforms,
                        enemygroup) == True:
                left = False
                right = False
                up = False

            for e in entities:
                screen.blit(e.image, camera.apply(e))
            for e in enemygroup:
                screen.blit(e.image, camera.apply(e))
                e.update(platforms, entities, enemygroup)

            health, maxL = player.getPlayerHealth()
            displayHeart.update("assets/img/heart.png", health, (WIN_WIDTH-150),
                                (16,16))
            displayFace.update("assets/img/face.png", maxLives, (30), (25, 25), 30)

            score = player.get_score()
            game_font = pygame.font.Font("freesansbold.ttf", 16)
            score_text = game_font.render(f"Score: {score}", False, (255, 255,
                                                                    255))
            screen.blit(score_text, (int(screen.get_width()/2)-50,0+8))

            pygame.display.update()

def drawCurtains(screen, levelIndex, text=None):
    window_size = 0
    color = (0, 0, 0)
    bg = pygame.image.load('assets/img/bg_gray3.jpg').convert()
    bg = pygame.transform.scale(bg, (screen.get_width(),
                                     screen.get_height()))
    screen.blit(bg,(0,0))
    for x in range(200):
        pygame.draw.rect(screen, color, (0, 0, screen.get_width(), window_size))
        pygame.display.flip() 
        window_size += 4
        time.sleep(0.005)

    if text == None:
        game_font = pygame.font.Font("freesansbold.ttf", 32)
        player_text = game_font.render("LEVEL " + str(levelIndex), False, (255,
                                                                           255,
                                                                           255))
        screen.blit(player_text, (screen.get_width()/2-50, int(screen.get_height()/2)))
        pygame.display.update()
        time.sleep(0.8)
    else:
        pp_sad1= pygame.image.load('assets/img/pp_sad1.png')
        pp_sad1 = pygame.transform.scale(pp_sad1, (MULTIPLIER*2, 32*5))
        pp_sad2= pygame.image.load('assets/img/pp_sad2.png')
        pp_sad2 = pygame.transform.scale(pp_sad2, (MULTIPLIER*2, 32*5))
        pp_sad3= pygame.image.load('assets/img/pp_sad3.png')
        pp_sad3 = pygame.transform.scale(pp_sad3, (MULTIPLIER*2, 32*5))
        pp_sad= [pp_sad1, pp_sad2, pp_sad3]
        #Copyright attribution: Skeleton sprite used is from artwork done by Irina Mir (irmirx)
        guard =  pygame.image.load("assets/img/guard1.png")
        guard = pygame.transform.scale(guard, (MULTIPLIER*3, 32*5))
        guard = pygame.transform.flip(guard, True, False)
        for indexCount in range (5):
            game_font = pygame.font.Font("freesansbold.ttf", 32)
            player_text = game_font.render(text, False, (255, 255, 255))
            screen.blit(player_text, (screen.get_width()/2-len(text)-200, int(screen.get_height()/2)))
            screen.blit(guard, (screen.get_width()-480, 130))
            screen.blit(pp_sad[2], (screen.get_width()-330, 135))
            pygame.display.update()
            time.sleep(0.8)


class Display(Entity):
    def __init__(self, filename, screen, count, xval, dimensions, margin=15):
        Entity.__init__(self)
        self.screen = screen
        #self.font = pygame.font.Font(None, 80)
        #self.image = self.font.render(string, 1, (255, 0, 0))
        for i in range(count):
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, dimensions)
            self.screen.blit(self.image,(xval+(i*margin), 10))
    def update(self, filename, count, xval, dimensions, margin=15):
        #self.image = self.font.render(string, 1, (255, 0, 0))
        for i in range(count):
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, dimensions)
            self.screen.blit(self.image,(xval+(i*margin), 10))

class Intro(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        global MULTIPLIER
        stand1= pygame.image.load('assets/img/adventBoy_stand1.png')
        stand1 = pygame.transform.scale(stand1, (MULTIPLIER*2, 32*5))
        stand2= pygame.image.load('assets/img/adventBoy_stand2.png')
        stand2 = pygame.transform.scale(stand2, (MULTIPLIER*2, 32*5))

        spritesheet = pygame.image.load("assets/img/smbenemiessheet.png")
        character = Surface((16,16),pygame.SRCALPHA)
        character.blit(spritesheet,(0,-34))
        character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
        goomba1 = character
        character = Surface((16,16),pygame.SRCALPHA)
        character.blit(spritesheet,(-30,-34))
        character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
        goomba2 = character


        spritesheet = pygame.image.load("assets/img/bubblebobble.png")
        character = Surface((20,20),pygame.SRCALPHA)
        character.blit(spritesheet,(-3,-1))
        character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
        bubble1 = character
        character = Surface((20,20),pygame.SRCALPHA)
        character.blit(spritesheet,(-23,-1))
        character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
        bubble2 = character

        pp_sad1 = pygame.image.load('assets/img/pp_sad1.png')
        pp_sad1 = pygame.transform.scale(pp_sad1, (MULTIPLIER*2, 32*5))
        pp_sad2= pygame.image.load('assets/img/pp_sad2.png')
        pp_sad2= pygame.transform.scale(pp_sad2, (MULTIPLIER*2, 32*5))

        self.stand = [stand1, stand2]
        self.pp_sad = [pp_sad1, pp_sad2]
        self.goomba = [goomba1, goomba2]
        self.bubble = [bubble1, bubble2]
        self.rect = self.stand[0].get_rect(center=(screen.get_width()/2, 370))
        self.recte = self.stand[0].get_rect(center=(screen.get_width()/2+20, 460))
        self.screen = screen

    def update(self, indexCount):
        if indexCount < 5:
            self.screen.blit(self.stand[indexCount%2], self.rect.center)
        elif indexCount > 5 and indexCount < 10:
            self.screen.blit(self.pp_sad[indexCount%2], self.rect.center)
        elif indexCount > 10 and indexCount < 15:
            self.screen.blit(self.goomba[indexCount%2], self.recte.center)
        elif indexCount > 15 and indexCount < 20:
            self.screen.blit(self.bubble[indexCount%2], self.recte.center)



def title_scene(screen):
    #screen = pygame.display.set_mode((800, 600))
    intro = Intro(screen)
    indexCount = 0

    # title screen
    bg = pygame.image.load('assets/img/bg_cs4.jpg').convert()
    bg = pygame.transform.scale(bg, (screen.get_width(),
                                     screen.get_height()))
    ltg1 = pygame.image.load('assets/img/lightning1.png')
    ltg2 = pygame.image.load('assets/img/lightning2.png')
    ltg = [ltg1, ltg2]


    title= pygame.image.load('assets/img/Castle-Raider.png')
    for count in range(20):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print ("Hope you enjoyed the Castle Raider !")
                pygame.mixer.music.stop()
                time.sleep(0.1)
                pygame.mixer.Sound('assets/ogg/death.ogg').play()
                drawCurtains(screen, 0, "Princess Ella is lost forever !")
                raise SystemExit("ESCAPE")

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print ("Cutscene cut short")
                    return
        screen.blit(bg,(0,0))
        rect = title.get_rect(center=(screen.get_width()/2-250,
                                      50))
        if count %7 == 0:
            ltgImg = ltg[count%2]
            x = random.randint(0, screen.get_width()-300)
            y = random.randint(200, 400) #screen.get_height()-1)
            angle = random.randint(0, 30)
            ltgImg = pygame.transform.scale(ltgImg, (80, y))
            ltgImg = pygame.transform.rotate(ltgImg, angle)
            screen.blit(ltgImg, (x, 0))
        game_font = pygame.font.Font("freesansbold.ttf", 32)
        player_text = game_font.render(" STARRING ", False, (255, 255, 255))
        screen.blit(player_text, (screen.get_width()/2-50, int(screen.get_height()/2)))

        game_font = pg.font.Font("freesansbold.ttf", 16)
        player_text = game_font.render("press SPACE to skip intro ", False, (255, 0, 0))
        screen.blit(player_text, (screen.get_width()-250,
                                       int(screen.get_height()-40)))

        intro.update(count)
        screen.blit(title, rect.center)
        pygame.display.update()
        time.sleep(0.4)

if __name__ == "__main__":
    main()
