import pygame as pg


def draw_text(screen, text, size, color, x, y):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


class CutSceneOne:
    
    def __init__(self, player, screen):

        # Variables
        self.name = 'test'
        self.step = 0
        self.timer = pg.time.get_ticks()
        self.cut_scene_running = True

        # If we need to control the player while a cut scene running
        self.player = player
        self.screen = screen

        # Dialogue
        self.text = {
            'one': "Princess Peach needs help, please hurry !",
            'two': "That's better, you are one floor closer to Princess Irma",
            'three': "That's better, now be careful 3",
            'four': "That's better, now be careful 4",
        }
        self.text_counter = 0

    def update(self):
        space = False
        
        # First cut scene step (dialogue)
        if self.step == 0:
            if int(self.text_counter) < len(self.text['one']):
                self.text_counter += 0.4
            else:
                if space:
                    self.step = 1

        # Second part (player movement)
        if self.step == 1:
            if True: 
                self.step = 2
                self.text_counter = 0
            #else:
            #    self.player.rect.x -= 5

        # Third part (dialogue)
        if self.step == 2:
            if int(self.text_counter) < len(self.text['two']):
                self.text_counter += 0.4
            else:
                if space:
                    # Finish the cut scene
                    self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        
        if self.step == 0:
            draw_text(
                screen,
                self.text['one'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                50,
                50
            )

        if self.step == 2:
            draw_text(
                screen,
                self.text['two'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                50,
                50
            )



class CutSceneManager:

    def __init__(self, player, screen):
        self.cut_scenes_complete = []
        self.cut_scene = None
        self.cut_scene_running = False

        # Drawing variables
        self.player = player
        self.screen = screen
        self.window_size = 0
        self.indexCount = 0
        self.counter = 0

    def start_cut_scene(self, cut_scene):
        if cut_scene.name not in self.cut_scenes_complete:
            self.cut_scenes_complete.append(cut_scene.name)
            self.cut_scene = cut_scene
            self.cut_scene_running = True

    def end_cut_scene(self):
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self, bg, walk, pp_sad, guard):
        for indexCount in range(155):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print ("Hope you enjoyed the Castle Raider !")
                    raise SystemExit("ESCAPE")

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        print ("Cutscene cut short")
                        return
            self.start_cut_scene(CutSceneOne(self.player, self.screen))
            self.draw(bg, walk, pp_sad, guard)
            if self.cut_scene_running:
                if self.window_size < self.screen.get_height()*0.3: self.window_size += 4
                if self.window_size >= 40:
                    self.cut_scene_running = self.cut_scene.update()
            else:
                self.end_cut_scene()
            pg.display.flip() 

            # animate the player
        #self.animate_player(self.screen, pp_sad, guard)

    def update_jump(self, rectj, screen, jump, indexCount, pp_sad, guard):
        import time
        win_width = self.screen.get_width()
        bg2 = pg.image.load('assets/img/bg_cs4.jpg').convert_alpha()
        bg2 = pg.transform.scale(bg2, (800, 660))
        bg3 = pg.image.load('assets/img/bg_cs2.png').convert_alpha()
        bg3 = pg.transform.scale(bg3, (800, 600))
        screen.blit(bg2,(0, 0))
        screen.blit(bg3,(0, 0))
        screen.blit(jump, rectj.center)
        screen.blit(guard, (win_width/2+20, 330))
        if indexCount % 2 == 0:
            screen.blit(pp_sad[indexCount%3], (win_width/2+200, 275))
        rectj.x += 5
        if indexCount < 20:
            rectj.y -= 5
        else:
            rectj.y += 5
        pg.display.update()
        time.sleep(0.05)

    def animate_player(self, screen, pp_sad, guard):
        win_width = self.screen.get_width()
        print("animating player")
        jump= pg.image.load('assets/img/adventBoy_jump.png')
        jump = pg.transform.scale(jump, (int(16*3*2), 32*5))
        rectj = jump.get_rect(center=(win_width/2-300, 503))
        # set background
        for indexCount in range(40):
            self.update_jump(rectj, screen, jump, indexCount, pp_sad, guard)

    def draw(self, bg, walk, pp_sad, guard):
        win_width = self.screen.get_width()
        bg2 = pg.image.load('assets/img/bg_cs4.jpg').convert_alpha()
        bg2 = pg.transform.scale(bg2, (800, 660))
        bg3 = pg.image.load('assets/img/bg_cs2.png').convert_alpha()
        bg3 = pg.transform.scale(bg3, (800, 600))
        self.screen.blit(bg2,(0, 0))
        self.screen.blit(bg3,(0, 0))
        self.screen.blit(walk[self.indexCount%2], (win_width/2-300, 500))
        self.screen.blit(guard, (win_width/2+50, 330))
        self.screen.blit(pp_sad[self.indexCount%3], (win_width/2+200, 275))
        game_font = pg.font.Font("freesansbold.ttf", 16)
        player_text = game_font.render("press SPACE to skip intro ", False, (255, 0, 0))
        self.screen.blit(player_text, (self.screen.get_width()-250,
                                       int(self.screen.get_height()-40)))
        if self.cut_scene_running:
            # Draw rect generic to all cut scenes
            pg.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen.get_width(), self.window_size))
            # Draw specific cut scene details
            self.cut_scene.draw(self.screen)
            self.counter += 1
            if (self.counter % 6) == 0:
                self.indexCount += 1



