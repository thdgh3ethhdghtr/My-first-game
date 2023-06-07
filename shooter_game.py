from pygame import *
from random import randint
from time import time as timer

HEIGHT = 700
WIDTH = 1200
FPS = 70

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

window = display.set_mode((WIDTH,HEIGHT))

img_bul = 'bullet.png'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_ast = 'asteroid.png'

display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(1200,700))   

class GameSprite(sprite.Sprite):
    def init(self, player_image, player_x, player_y, size_x,size_y,player_speed):
        sprite.Sprite.init(self)
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
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
        if keys[K_RIGHT] and self.rect.x < WIDTH - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            ship.fire()

    def fire(self):
        bullet = Bullet(img_bul,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > HEIGHT:
            self.rect.x = randint(80, WIDTH - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


font.init()
font2 = font.Font(None,36)    

#bullet = 0
number = 9
score = 0
lost = 0

def stats():
    global score
    for monster in monsters:
        for bullet in bullets:
            if monster.rect.colliderect(bullet.rect):
                score += 1 

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)


monsters = sprite.Group()
for  i in range(1,8):
    

    ship = Player (img_hero,5,HEIGHT - 100,80,100,10)
finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        num_fire = num_fire + 1 
                        fire_sound.play()
                        ship.fire()

        if num_fire >= 5 and rel_time == False:
            last_time = timer()
            rel_time = True
        
    if not finish:
        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy,randint(80,WIDTH - 80),-40,80,50,randint(1,5))
            monster.add(monsters)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= goal  

        sprites_list = sprite.spritecollide(
            ship,monsters,False
        )
        text = font2.render('Счeт:' + str(score),1,(255,69,0))
        window.blit(text,(10,10))
        text_lose = font2.render('Пропустил:' + str(lost),1,(255,0,255))
        window.blit(text_lose,(10,50))


        rel_time = False
        num_fire = 0


        

        monster.reset()
        asteroids.update()
        asteroids.draw(window)
        display.update()

    time.delay(20)