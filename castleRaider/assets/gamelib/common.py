import pygame
from pygame import *
import time
import warnings
warnings.simplefilter("ignore")
DEBUG = False
WIN_WIDTH = 256*3
WIN_HEIGHT = 224*3
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
DEAD = pygame.USEREVENT + 1
NEXT_LEVEL = pygame.USEREVENT + 2
HURT = pygame.USEREVENT + 3
REDRAW_DOOR = pygame.USEREVENT + 4
ONE_UP = pygame.USEREVENT + 5
MULTIPLIER = (16*3)
WHITE_COLOR = (255, 255, 204)

#nextLevel = True
#exitObject = None

spritesheet = pygame.image.load("assets/img/adventBoy3.png")

character = Surface((120, 190),pygame.SRCALPHA)
character.blit(spritesheet,(-112, -278)) #(-46,-18))
character = pygame.transform.scale(character, (MULTIPLIER+30,32*3))
adventBoy_stand1 = character

character = Surface((120, 190),pygame.SRCALPHA)
character.blit(spritesheet,(-115, -57)) #(-241,-157))   #-239, -51
character = pygame.transform.scale(character, (MULTIPLIER+30,32*3))
adventBoy_walk1 = character

character = Surface((120, 190),pygame.SRCALPHA)
character.blit(spritesheet,(-336, -60)) #(-52,-157))   #-239, -52
character = pygame.transform.scale(character, (MULTIPLIER+30,32*3))
adventBoy_walk2 = character

character = Surface((120, 190),pygame.SRCALPHA)
character.blit(spritesheet,(-554, -56)) #(-147,-157))   #-239, -51
character = pygame.transform.scale(character, (MULTIPLIER+30,32*3))
adventBoy_walk3 = character

character = Surface((135, 190),pygame.SRCALPHA)
character.blit(spritesheet,(-117, -490)) #(-138,-292))   #-239, -52
character = pygame.transform.scale(character, (MULTIPLIER+30,32*3))
adventBoy_jump1 = character

'''
character = Surface((80,97),pygame.SRCALPHA)
character.blit(spritesheet2,(-370,-44))   #-239, -52
character = pygame.transform.scale(character, (MULTIPLIER,32*3))
adventBoy_dead1 = character

character = Surface((80,97),pygame.SRCALPHA)
character.blit(spritesheet2,(-472,-44))   #-239, -52
character = pygame.transform.scale(character, (MULTIPLIER,32*3))
adventBoy_dead2 = character
'''

spritesheet = pygame.image.load("assets/img/smbenemiessheet.png")

character = Surface((16,16),pygame.SRCALPHA)
character.blit(spritesheet,(0,-34))
character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
goombawalk1 = character

character = Surface((16,16),pygame.SRCALPHA)
character.blit(spritesheet,(-30,-34))
character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
goombawalk2 = character

character = Surface((16,16),pygame.SRCALPHA)
character.blit(spritesheet,(-60,-28))
character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
goombaflat1 = character

spritesheet = pygame.image.load("assets/img/bubblebobble.png")

character = Surface((20,20),pygame.SRCALPHA)
character.blit(spritesheet,(-3,-1))
character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
#character = pygame.transform.flip(character, True, False)
bubblewalk1 = character

character = Surface((20,20),pygame.SRCALPHA)
character.blit(spritesheet,(-23,-1))
character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
#character = pygame.transform.flip(character, True, False)
bubblewalk2 = character

character = Surface((20,20),pygame.SRCALPHA)
character.blit(spritesheet,(-46,-253))
character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
bubbleblast = character
character = pygame.transform.scale(character, (MULTIPLIER*2,MULTIPLIER*2))
adventBoy_dead1 = character
adventBoy_dead2 = character

spritesheet = pygame.image.load("assets/img/zombie.png")

character = Surface((55,90),pygame.SRCALPHA)
character.blit(spritesheet,(-228,-104))
character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
#character = pygame.transform.flip(character, True, False)
zombiewalk1 = character

character = Surface((55,90),pygame.SRCALPHA)
character.blit(spritesheet,(-303,-104))
character = pygame.transform.scale(character, (MULTIPLIER,MULTIPLIER))
#character = pygame.transform.flip(character, True, False)
zombiewalk2 = character

