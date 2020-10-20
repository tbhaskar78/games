import pygame
import sys
import random
import time
from math import sin, cos, pi
screen_width  = 480
screen_height = 480 

gridsize = 20
grid_width = int(screen_width/gridsize)
grid_height = int(screen_height/gridsize)

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)
color1 = [(93,216,228),(84,194,205)]
color3 = [(178,102,255),(204,153,255)]
color5 = [(128, 128, 128),(192, 192, 192)]
color7 = [(226,171,171),(144,136,136)]
veggies = ['assets/img/broccoli.png', 'assets/img/strawberry.png', 'assets/img/cabbage.png', 'assets/img/cherry.png',
        'assets/img/veggie.png']

class Snake():
    def __init__(self):
        self.length = 1
        self.life = 3
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        self.score = 0
        self.cumulative_score = 0
        self.top_score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length >= 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.cumulative_score += self.score
        if self.score > self.top_score:
            self.top_score = self.score
        self.score = 0
        self.length = 1
        self.life -= 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        pygame.mixer.Sound('assets/ogg/fail.ogg').play()

    def reduce(self):
        self.score -= 2
        x = self.length
        self.length = (x-2)
        pygame.mixer.Sound('assets/ogg/fail.ogg').play()

    def draw_regular_polygon(self, surface, color, position):
        n, r = 6, int(10) #radius
        x, y = position
        pygame.draw.polygon(surface, color, [
            (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
            for i in range(n)
        ])

    def draw(self,surface):
        count = 0
        for p in self.positions:
            r = pygame.Rect((int(p[0]), int(p[1])), (int(gridsize), int(gridsize)))
            if count == 0:
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, (255,0, 0), r, 1)
            else:
                #pygame.draw.ellipse(surface, (51, 0, 51, 100), r)
                pygame.draw.ellipse(surface, (0, 102, 0, 100), r)
            count += 1

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface, imageName):
        image = pygame.image.load(imageName)
        image = pygame.transform.scale(image, (int(grid_width-5), int(grid_height-5)))
        surface.blit(image, (self.position[0], self.position[1]))

class Poison():
    def __init__(self):
        self.position = (0,0)
        self.color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface, imageName):
        image = pygame.image.load(imageName)
        image = pygame.transform.scale(image, (int(grid_width-5), int(grid_height-5)))
        surface.blit(image, (self.position[0], self.position[1]))

def drawGrid(surface, colorA, colorB):
    #image = pygame.image.load('grass.png')
    #surface.blit(image, (0,0))
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,colorA, r)
                #pygame.draw.rect(surface,(255,102,102), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, colorB, rr)
                #pygame.draw.rect(surface, (255,204,204), rr)

def main():
    pygame.mixer.pre_init(44100, -16, 2, 128)
    pygame.init()
    pygame.display.set_caption('Snake')

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    colorA = color1[0]
    colorB = color1[1]
    drawGrid(surface, colorA, colorB)

    snake = Snake()
    food = Food()
    food2 = Food()
    broccoli = Food()
    poison = Poison()
    potion = Poison()
    count = 0
    poisonDrawn = 0
    potionDrawn = 0
    broccoliDrawn = 0
    veggieIndex = 0

    myfont = pygame.font.SysFont("monospace",16)
    game_font = pygame.font.Font("freesansbold.ttf", 32)


    pygame.mixer.music.load('assets/ogg/clown.ogg')
    pygame.mixer.music.play(-1)
    while (True):
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface, colorA, colorB)
        snake.move()

        # broccoli
        if snake.get_head_position() == broccoli.position and broccoliDrawn == 1:
            pygame.mixer.Sound('assets/ogg/success.ogg').play()
            broccoliDrawn = 0
            veggieIndex = random.choice([0, 1, 2, 3, 4])
            bonus = game_font.render("You ate your Veggies!", False, (255,0,0));
            screen.blit(bonus, (int(screen_width/2)-150, int(screen_height/2)-20))
            bonus2 = game_font.render("BONUS 5 points!", False, (255,0,0));
            screen.blit(bonus2, (int(screen_width/2)-150, int(screen_height/2)+20))
            pygame.display.update()
            time.sleep(1)
            pygame.mixer.Sound('assets/ogg/eat_apple.ogg').play()
            snake.length += 5
            snake.score += 5
            broccoli.randomize_position()
            if broccoli.position[0] == potion.position[0]:
                broccoli.randomize_position()
            if broccoli.position[0] == potion.position[0]:
                broccoli.randomize_position()
            if broccoli.position[0] == poison.position[0]:
                broccoli.randomize_position()
            if broccoli.position[0] == food2.position[0]:
                broccoli.randomize_position()
        # food 1
        if snake.get_head_position() == food.position:
            pygame.mixer.Sound('assets/ogg/eat_apple.ogg').play()
            snake.length += 1
            snake.score += 1
            food.randomize_position()
            if food.position[0] == broccoli.position[0]:
                food.randomize_position()
            if food.position[0] == potion.position[0]:
                food.randomize_position()
            if food.position[0] == poison.position[0]:
                food.randomize_position()
            if food.position[0] == food2.position[0]:
                food.randomize_position()

        # food 2
        if snake.get_head_position() == food2.position:
            pygame.mixer.Sound('assets/ogg/eat_apple.ogg').play()
            snake.length += 1
            snake.score += 1
            food2.randomize_position()
            if food2.position[0] == broccoli.position[0]:
                food2.randomize_position()
            if food2.position[0] == potion.position[0]:
                food2.randomize_position()
            if food2.position[0] == poison.position[0]:
                food2.randomize_position()
            elif food2.position[0] == food.position[0]:
                food2.randomize_position()

        # poison
        if snake.get_head_position() == poison.position and poisonDrawn == 1:
            poisonDrawn = 0
            tempscore = snake.score
            snake.reset()
            poison.randomize_position()
            if poison.position[0] == broccoli.position[0]:
                poison.randomize_position()
            if poison.position[0] == potion.position[0]:
                poison.randomize_position()
            if poison.position[0] == food.position[0]:
                poison.randomize_position()
            if poison.position[0] == food2.position[0]:
                poison.randomize_position()

        # potion
        if snake.get_head_position() == potion.position and potionDrawn == 1:
            potionDrawn = 0
            pygame.mixer.Sound('assets/ogg/sneeze.ogg').play()
            minus = game_font.render("oops...ATE A CHILLI!", False, (255,0,0));
            minus2 = game_font.render("Reducing 2 points", False, (255,0,0));
            screen.blit(minus, (int(screen_width/2)-150, int(screen_height/2)-20))
            screen.blit(minus2, (int(screen_width/2)-120, int(screen_height/2)+20))
            pygame.display.update()
            time.sleep(1)
            snake.reduce()
            drawGrid(surface, colorA, colorB)
            potion.randomize_position()
            if potion.position[0] == broccoli.position[0]:
                potion.randomize_position()
            if poison.position[0] == potion.position[0]:
                potion.randomize_position()
            if potion.position[0] == food.position[0]:
                potion.randomize_position()
            if potion.position[0] == food2.position[0]:
                potion.randomize_position()

        if (snake.length+1) % 10 == 0 and count == 0:
            colors = random.choice([color1, color3, color5, color7])
            colorA = colors[0]
            colorB = colors[1]
            count = 1
        elif (snake.length) % 10 == 0:
            count = 0

        if snake.length > 1:
            poison.draw(surface, 'assets/img/potion.png')
            poisonDrawn = 1

        if snake.length > 7:
            potion.draw(surface, 'assets/img/chilli.png')
            potionDrawn = 1

        if snake.life <= 0:
            pygame.mixer.Sound('assets/ogg/fail2.ogg').play()
            surface.fill((255,255,255))
            game_end = game_font.render("Game Ends!", False, (255,0,0));
            game_top_score = game_font.render("Your top score {0}".format(snake.top_score), False, (255,0,0));
            game_top_cum_score = game_font.render("Your cumulative score {0}".format(snake.cumulative_score), False, (255,0,0));
            screen.blit(game_end, (int(screen_width/2)-90, int(screen_height/2)-20))
            screen.blit(game_top_score, (int(screen_width/2)-100, int(screen_height/2)+20))
            screen.blit(game_top_cum_score, (int(screen_width/2)-200, int(screen_height/2)+60))
            pygame.display.update()
            time.sleep(4)
            pygame.quit()
            sys.exit()

        snake.draw(surface)
        food.draw(surface, 'assets/img/food.png')
        food2.draw(surface,'assets/img/hotdog.png')
        if snake.length % 7 == 0 or broccoliDrawn == 1:
            broccoli.draw(surface, veggies[veggieIndex])
            broccoliDrawn = 1
        
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), False, (0,0,0))
        text2 = myfont.render("Life {0}".format(snake.life), False, (0,0,0))
        screen.blit(text, (5,10))
        screen.blit(text2, (5,25))
        pygame.display.update()

main()

