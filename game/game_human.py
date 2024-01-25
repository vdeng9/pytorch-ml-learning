#cargame for human
import pygame
from pygame.locals import *
import random, time, os, sys

pygame.init()

movementUnit = 5
SPEED = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
global enemySpd
enemySpd = movementUnit
global points
points = 0
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

class cargame:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT
        self.score = points
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('car game')
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.enemy = Enemy()
        self.bg = Background()
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.enemy)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemy)

    def playStep(self):
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                global enemySpd
                enemySpd += 0.5   
                print(enemySpd)  
            if event.type == QUIT:
                pygame.quit()

        gameover = False
        if pygame.sprite.spritecollideany(self.player,self.enemies):
            gameover = True
            pygame.mixer.Sound(os.path.join(sys.path[0], "crash.wav")).play()
            time.sleep(0.5)
                        
            self.display.fill(RED)
            self.display.blit(game_over, (30,250))

            pygame.display.update()
            for entity in self.all_sprites:
                    entity.kill() 
            time.sleep(1)
            return gameover, self.score
        
        self.updateUi()
        self.clock.tick(SPEED)
        
        return gameover, self.score
          
    def updateUi(self):
        self.bg.update()
        self.bg.render(self.display)
        self.score = points
        displayScore = font_small.render(str(self.score), True, BLACK)
        self.display.blit(displayScore, (10,10))
        for entity in self.all_sprites:
            self.display.blit(entity.image, entity.rect)
            entity.move()
        pygame.display.update()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(os.path.join(sys.path[0], "Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH-50), 0)  

    def move(self):
        global points
        self.rect.move_ip(0,enemySpd)
        if (self.rect.top > SCREEN_HEIGHT):
            points += 1
            self.rect.top = 0
            self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(os.path.join(sys.path[0], "Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-100)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top > 0:
            if pressed_keys[K_UP] or pressed_keys[K_w]:
                self.rect.move_ip(0, -movementUnit)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN] or pressed_keys[K_s]:
                self.rect.move_ip(0, movementUnit)
        if self.rect.left > 50:
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.rect.move_ip(-movementUnit, 0)
        if self.rect.right < SCREEN_WIDTH - 50:        
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.rect.move_ip(movementUnit, 0)

class Background():
      def __init__(self):
            self.bgimage = pygame.image.load(os.path.join(sys.path[0], "AnimatedStreet.png"))
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = self.rectBGimg.height
            self.bgX2 = 0
 
            self.moving_speed = movementUnit
         
      def update(self):
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height
             
      def render(self, display):
            display.blit(self.bgimage, (self.bgX1, self.bgY1))
            display.blit(self.bgimage, (self.bgX2, self.bgY2))

game = cargame(SCREEN_WIDTH, SCREEN_HEIGHT)
while True:
    gameover, score = game.playStep()
    if gameover:
        break
print("final score: ", score)    