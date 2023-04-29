from pygame import *
from random import *
from time import time as timer 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 100, 15, 20)
        bullets.add(bullet)

lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)


font.init()
font1 = font.SysFont('Arial',36)
text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))

ship = Player("rocket.png",5,400,10, 80, 100)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(80,620),-40,randint(1,3), 80, 50)
    monsters.add(monster)
window = display.set_mode((700, 500))
display.set_caption('Shooter')
backgraund = transform.scale(image.load('galaxy.jpg'), (700,500))

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png',randint(80,620),-40,randint(1,3), 80, 50)
    asteroids.add(asteroid)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

font.init()
font = font.SysFont('Arial', 80)
win = font.render('You win!', True, (255,255,0))
lose = font.render('You lose', True, (255,0,0))

FPS = 60
clock = time.Clock()
run = True
finish = False
num_fire = 0
rel_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 30 and rel_time == False:
                    rel_time = True
                    last_time = timer()
    if finish != True:
        sprites_list = sprite.spritecollide(ship, monsters, False)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        prites_list = sprite.spritecollide(ship,asteroids, False)
        for i in collides:
            score += 1
            monster = Enemy('ufo.png',randint(80,620),-40,randint(1,4), 80, 50)
            monsters.add(monster)
        window.blit(backgraund,(0, 0))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.update()
        asteroids.update()
        bullets.draw(window)
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_score = font1.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))
        window.blit(text_score, (10,20))
        if score >= 10:
            finish = True
            window.blit(win, (10,50))
        if lost >=3 or sprites_list or prites_list:
            finish = True
            window.blit(lose, (10,50))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time <3:
                reload = font1.render('Wait,reload...',1,(150,0,0))
                window.blit(reload, (260,460))
            else:
                rel_time = False
                num_fire = 0
    display.update()
    clock.tick(FPS)