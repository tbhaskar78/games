from assets.gamelib.common import *
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y, livesLeft, screen, score):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.faceright = True
        self.onGround = False
        self.airborne = False
        self.takingdamage = False
        self.counter = 0
        self.fallingcount = 0
        self.image = adventBoy_stand1
        self.rect = Rect(x, y, MULTIPLIER+30, 32*3) #16*3, 32*4-35)
        self.lifetotal = ["", "l", "ll", "lll", "llll", "lllll", "llllll", "lllllll", "llllllll", "lllllllll"]
        self.currentlifetotal = 9
        self.maxLives = livesLeft
        self.key = False
        self.gotKey = False
        self.screen = screen
        self.score = score

    def get_score(self):
        return self.score

    def update(self, up, down, left, right, running, platforms, enemygroup):
        if up:
            # only jump if on the ground
            if self.onGround: 
                pygame.mixer.Sound('assets/ogg/jump.ogg').play()
                self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
            self.faceright = False
        if right:
            self.xvel = 8
            self.faceright = True
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: 
                self.yvel = 100
        if not(left or right):
            self.xvel = 0

        # yvel == 1.2 is the absolute ground
        if self.yvel < 0 or self.yvel > 1.2: 
            self.fallingcount += 1
            self.airborne = True
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        left = False
        right = False
        up  = False
        if self.collide(self.xvel, 0, platforms, enemygroup) == False:
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;

            # do y-axis collisions
            if self.collide(0, self.yvel, platforms, enemygroup) == False:
                self.animate()
            return False
        else:
            return True

    def collide(self, xvel, yvel, platforms, enemygroup):
        global DEBUG
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock) and self.gotKey == True:
                    if DEBUG == True:
                        print("Exit block, got Key")
                    self.gotKey = False
                    self.takingdamage = False
                    pygame.event.post(pygame.event.Event(NEXT_LEVEL))
                    return True
                if isinstance(p, SpearBlock):
                    if DEBUG == True:
                        print("Spear block")
                    pygame.mixer.Sound('assets/ogg/fail.ogg').play()
                    self.currentlifetotal = 0
                    pygame.event.clear()
                    self.updatecharacter(adventBoy_dead2)
                    pygame.event.post(pygame.event.Event(DEAD))
                    return True
                if isinstance(p, Food):
                    self.score += 100
                    if self.currentlifetotal < 9:
                        self.currentlifetotal += 1
                    print("1 UP")
                    p.animate()
                if isinstance(p, KeyBlock):
                    self.score += 1000
                    p.animate()
                    self.gotKey = p.getKeyStatus()
                if xvel > 0:
                    self.rect.right = p.rect.left
                    if DEBUG==True:
                        print("Player collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    if DEBUG==True:
                        print("Player collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    if self.fallingcount >= 115:
                            self.currentlifetotal -= 1
                            if self.currentlifetotal <= 0:
                                self.currentlifetotal = 0
                                self.updatecharacter(adventBoy_dead2)
                                pygame.event.post(pygame.event.Event(DEAD))
                            else:
                                self.updatecharacter(adventBoy_dead1)
                                pygame.event.post(pygame.event.Event(HURT))
                    self.fallingcount = 0
                    self.airborne = False
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

        if self.takingdamage == True:
            if self.faceright == False:
                self.faceright = True
            else:
                self.faceright = False

            if xvel > 0:
                self.xvel += 40
                self.yvel -= 3
            else:
                self.xvel -= 40
                self.yvel -= 3
            self.takingdamage = False
            self.updatecharacter(adventBoy_walk1)

        for e in enemygroup:
            if pygame.sprite.collide_rect(self, e):
                self.score += 10
                self.fallingcount = 0
                dif = self.rect.bottom - e.rect.top
                if dif <= 8:
                    self.yvel = -8
                elif self.takingdamage == False:
                    self.takingdamage = True
                    # destroy the enemy because of the hit
                    e.destroy_now()

                    self.currentlifetotal = self.currentlifetotal - 1
                    pygame.event.clear()
                    pygame.mixer.Sound('assets/ogg/ouch.ogg').play()
                    left = False
                    right = False
                    up = False
                    if self.currentlifetotal <= 0:
                        self.currentlifetotal = 0
                        self.updatecharacter(adventBoy_dead2)
                        pygame.event.post(pygame.event.Event(DEAD))
                        return True
                    else:
                        self.updatecharacter(adventBoy_dead1)
                        self.screen.blit(adventBoy_dead1, self.rect)
                        pygame.display.update(self.rect)
                        return True
        return False

    def animate(self):
        try:
            if self.xvel > 0 or self.xvel < 0:
                self.walkloop()
                if self.airborne:
                    self.updatecharacter(adventBoy_jump1)
            else:
                self.updatecharacter(adventBoy_stand1)
                if self.airborne: 
                    self.updatecharacter(adventBoy_jump1)
        except:
            print("Caught exception")

    def walkloop(self):
        if self.counter == 5:
            self.updatecharacter(adventBoy_walk3)
        elif self.counter == 10:
            self.updatecharacter(adventBoy_walk2)
        elif self.counter == 15:
            self.updatecharacter(adventBoy_walk1)
            self.counter = 0
        self.counter = self.counter + 1

    def updatecharacter(self, ansurf):
        if not self.faceright: 
            try:
                ansurf = pygame.transform.flip(ansurf,True,False)
            except:
                print("caught an exception")
        self.image = ansurf

    def getPlayerHealth(self):
        return self.currentlifetotal, self.maxLives

class Bubble(Entity):
    def __init__(self, x, y, screen):
        Entity.__init__(self)
        self.xvel = -1
        self.yvel = 0
        self.onGround = False
        self.destroyed = False
        self.counter = 0
        self.image = bubblewalk1
        self.faceRight = True
        self.screen = screen
        self.rect = Rect(x, y, 16*3, 16*3)

    def update(self, platforms, entities, enemygroup):
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100

        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms, entities, enemygroup)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms, entities, enemygroup)

        self.animate()

    def collide(self, xvel, yvel, platforms, entities, enemygroup):
        global DEBUG
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = -abs(xvel)
                    self.faceRight = True
                    if DEBUG==True:
                        print("Bubble collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = abs(xvel)
                    self.faceRight = False
                    if DEBUG==True:
                        print("Bubble collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.airborne = False
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
        for p in entities:
            if pygame.sprite.collide_rect(self, p):
                dif = p.rect.bottom - self.rect.top
                if dif <= 8:
                    self.destroyed = True
                    self.counter = 0
                    self.xvel = 0
        for e in enemygroup:
            if pygame.sprite.collide_rect(self, e):
                dif = self.rect.bottom - e.rect.top
                if xvel > 0:
                    #self.rect.right = p.rect.left
                    #self.xvel = -abs(xvel)
                    self.faceRight = False
                if xvel < 0:
                    #self.rect.left = p.rect.right
                    #self.xvel = abs(xvel)
                    self.faceRight = True
                    
    def animate(self):

        if not self.destroyed: self.walkloop()
        else: self.destroyloop()

    def walkloop(self):
        if self.counter == 10:
            self.updatecharacter(bubblewalk1)
        elif self.counter == 20:
            self.updatecharacter(bubblewalk2)
            self.counter = 0
        self.counter = self.counter + 1

    def destroy_now(self):
        self.updatecharacter(bubbleblast)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update(self.rect)
        time.sleep(0.1)
        self.kill()

    def destroyloop(self):
        if self.counter == 0:
            self.updatecharacter(bubbleblast)
        elif self.counter == 10: self.kill()
        self.counter = self.counter + 1

    def updatecharacter(self, ansurf):
        #self.image = ansurf
        if not self.faceRight:
            try:
                ansurf = pygame.transform.flip(ansurf,True,False)
            except:
                print("caught an exception")
        self.image = ansurf

class Goomba(Entity):
    def __init__(self, x, y, screen):
        Entity.__init__(self)
        self.xvel = -1
        self.yvel = 0
        self.onGround = False
        self.destroyed = False
        self.counter = 0
        self.image = goombawalk1
        self.rect = Rect(x, y, 16*3, 16*3)
        self.screen = screen

    def update(self, platforms, entities, enemygroup):
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100

        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms, entities)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms, entities)

        self.animate()

    def collide(self, xvel, yvel, platforms, entities):
        global DEBUG
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                #if isinstance(p, ExitBlock):
                #    pygame.event.post(pygame.event.Event(DEAD))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = -abs(xvel)
                    if DEBUG==True:
                        print("Goomba collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = abs(xvel)
                    if DEBUG==True:
                        print("Goomba collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.airborne = False
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
        for p in entities:
            if pygame.sprite.collide_rect(self, p):
                dif = p.rect.bottom - self.rect.top
                if dif <= 8:
                    self.destroyed = True
                    self.counter = 0
                    self.xvel = 0
                    
    def animate(self):

        if not self.destroyed: self.walkloop()
        else: self.destroyloop()

    def walkloop(self):
        if self.counter == 10:
            self.updatecharacter(goombawalk1)
        elif self.counter == 20:
            self.updatecharacter(goombawalk2)
            self.counter = 0
        self.counter = self.counter + 1

    def destroy_now(self):
        self.updatecharacter(bubbleblast)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update(self.rect)
        time.sleep(0.1)
        self.kill()

    def destroyloop(self):
        if self.counter == 0:
            self.updatecharacter(goombaflat1)
        elif self.counter == 10: self.kill()
        self.counter = self.counter + 1

    def updatecharacter(self, ansurf):
        self.image = ansurf

class Platform(Entity):
    def __init__(self, x, y, filename, dimx=16*3, dimy=16*3, key=False,
                 exit=False, screen=None):
        Entity.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image,(dimx, dimy))
        self.rect = Rect(x, y, dimx, dimy)
        if exit == True:
            return self.image
        elif key == True:
            return self.image

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y, screen, filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.dimx = 100
        self.dimy = 140
        self.image = Platform.__init__(self, x, y, filename,
                                      self.dimx, self.dimy, False, True,
                                      self.screen)

        #pygame.display.update(pygame.Rect(self.x, self.y, self.dimx, self.dimy))
        #self.screen.blit(self.image, (self.x, self.y))
        #pygame.display.update(pygame.Rect(self.x, self.y, self.dimx, self.dimy))
        #self.image.fill(Color("#0033FF"))

    def animate(self, pRect):
        y = pRect.y
        dimx = pRect.w
        dimy = pRect.h
        '''
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image,(dimx, dimy))
        self.rect = Rect(x, y, dimx, dimy)
        '''
        #self.kill()

    def getDimensions(self):
        return self.x, self.y, self.dimx, self.dimy


class KeyBlock(Platform):
    def __init__(self, x, y, screen):
        self.gotKey = False
        self.screen = screen
        self.x = x
        self.y = y
        self.dimx = 16*3
        self.dimy = 16*3
        self.image = Platform.__init__(self, x, y, "assets/img/key.png", self.dimx,
                          self.dimy, True)
        #self.image.fill(Color("#0033FF"))

    def animate(self):
        global gotkey
        #self.kill()
        self.gotKey = True
        pygame.mixer.Sound('assets/ogg/success.ogg').play()
        pygame.event.post(pygame.event.Event(REDRAW_DOOR))

    def getKeyStatus(self):
        if self.gotKey == True:
            return True
        else:
            return False

class Food(Platform):
    def __init__(self, x, y, screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.dimx = 16*3
        self.dimy = 16*3
        self.image = Platform.__init__(self, x, y, "assets/img/doughnut.png", self.dimx,
                          self.dimy, True)
        #self.image.fill(Color("#0033FF"))

    def animate(self):
        pygame.mixer.Sound('assets/ogg/success.ogg').play()
        pygame.event.post(pygame.event.Event(ONE_UP))


class SpearBlock(Platform):
    def __init__(self, x, y, screen, filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.dimx = 50
        self.dimy = 40
        Platform.__init__(self, x, y, filename,
                          self.dimx, self.dimy, False, False,
                          self.screen)

        #pygame.display.update(pygame.Rect(self.x, self.y, self.dimx, self.dimy))
        #self.screen.blit(self.image, (self.x, self.y))
        #pygame.display.update(pygame.Rect(self.x, self.y, self.dimx, self.dimy))

