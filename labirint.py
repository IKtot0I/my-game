from pygame import *
#faf
window = display.set_mode((700,500))
BLUE = (200,255,255)

display.set_caption('Лабиринт')
run = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self,picture,x,y,width,height):
        super().__init__()
        self.image = transform.scale(image.load(picture),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def __init__(self,picture,x,y,width,height,x_speed,y_speed):
        super().__init__(picture,x,y,width,height)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom,p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top,p.rect.bottom)
    def fire(self):
        bullet = Bullet('weapon.png',self.rect.right,self.rect.centery,15,20,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self,picture,x,y,width,height,speed):
        super().__init__(picture,x,y,width,height)
        self.speed = speed
        self.direction = 'left'
    def update(self):
        if self.rect.x <= 400:
            self.direction = 'right'
        if self.rect.x >= 600:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self,picture,x,y,width,height,speed):
        super().__init__(picture,x,y,width,height)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700 + 15:
            self.kill()

wall_1 = GameSprite('platform_h.png',520,150,180,50)
wall_2 = GameSprite('platform_v.png',350,80,50,420)
wall_3 = GameSprite('platform_h.png',130,250,250,50)
wall_11 = GameSprite('platform_v.png',-60,-30,50,750)
wall_12 = GameSprite('platform_v.png',710,-30,50,750)
wall_13 = GameSprite('platform_h.png',-30,500,750,50)
wall_14 = GameSprite('platform_h.png',-30,-50,750,50)

player = Player('hero.png',100,400,60,60,0,0)
final = GameSprite('enemy2.png',500,430,65,65)
monster = Enemy('enemy.png',500,260,65,65,10)
win = transform.scale(image.load('thumb.jpg'),(700,500))
lose = transform.scale(image.load('game-over_1.png'),(700,500))

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)
barriers.add(wall_11)
barriers.add(wall_12)
barriers.add(wall_13)
barriers.add(wall_14)
bullets = sprite.Group()

monsters = sprite.Group()
monsters.add(monster)
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                player.y_speed = -15
            elif e.key == K_DOWN:
                player.y_speed = 15
            elif e.key == K_LEFT:
                player.x_speed = -10
            elif e.key == K_RIGHT:
                player.x_speed = 10
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0
            elif e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0



    if finish != True:
        window.fill(BLUE)
        player.update()
        bullets.update()
        player.reset()
        bullets.draw(window)
        barriers.draw(window)
        final.reset()
        sprite.groupcollide(bullets,monsters,True,True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets,barriers,True,False)
        if sprite.collide_rect(player,final):
            finish = True
            window.blit(win,(0,0))
        elif sprite.spritecollide(player,monsters,False):
            finish = True
            window.blit(lose,(0,0))

    display.update()