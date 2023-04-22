from pygame import*
from random import randint
from time import time as timer# Импорты


init()


window = display.set_mode((700, 700))#Создание окна
display.set_caption('пиу пау')#название приложения собстна
display.set_icon(image.load('ufo.png'))
background = transform.scale(image.load('bulab.jpg'), (700, 700))#тут у нас расширение заднего фона

clock = time.Clock()#клок
lost = 0
life = 3
killed = 0
num_fire = 0

font.init()
font1 = font.SysFont("Arial", 30)

class GameSprite(sprite.Sprite):#основной класс
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))#тут размер
        self.speed = speed#скорость 
        self.rect = self.image.get_rect()
        self.rect.x = player_x#Х ну ниже у собстна
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):#лево право верх низ ракета
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
        #if keys[K_w] and self.rect.y < 650:
            #self.rect.y -= self.speed
        #if keys[K_s] and self.rect.y > 0:
            #self.rect.y += self.speed      
    def fire(self):#выстрелы пиу пиу
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 12)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed 
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(80, 620)


player = Player('rocket.png', 310, 600, 100, 100, 10)#Параметры для ракеты
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), 0, 80, 50, randint(1, 2))
    monsters.add(monster)
for i in range(5):
    asteroid = Asteroid('asteroid.png', randint(80, 600), -50, 80, 50, randint(2, 4))
    asteroids.add(asteroid)

bullets = sprite.Group()


#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()




fps = 60
game = True
finish = False
rel_time = False


fire_snd = mixer.Sound('fire.ogg')


while game:#основной цЫкл
    for e in event.get():#конец игры
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_w:
                if num_fire <= 10 and rel_time == False:
                    num_fire += 1
                    player.fire()            
                    fire_snd.play()
                if num_fire > 10 and rel_time == False:
                    rel_time = True
                    last_time = timer()
    if not finish:
        window.blit(background, (0, 0))#задний фон

        player.reset()#игрок 
        player.update()

        monsters.update()
        monsters.draw(window)

        bullets.draw(window)
        bullets.update()
        
        asteroids.draw(window)
        asteroids.update()
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render("ПАДАЖДИ потратил все патроны бош!", 1, (255,0, 0))
                window.blit(reload, (250, 500))
            else:
                rel_time = False
                num_fire = 0
            
        collides = sprite.groupcollide(bullets, monsters, True, True)
        for col in collides:
            enemy = Enemy('ufo.png', randint(50,600), -50, 80, 50, randint(1, 3))
            monsters.add(enemy)
            killed += 1

        if sprite.spritecollide(player, monsters, True):
            life -= 1

        life1 = font1.render('Жизнь: ' + str(life), 1, (0, 0, 0))
        window.blit(life1, (10,10))#жизни

        score = font1.render('Пропущено: ' + str(lost), 1, (0, 0, 0))
        window.blit(score, (10,40))#пропуски (можно лешится зубов)

        killed_dead = font1.render('Умер прасти: ' + str(killed), 1, (0, 0, 0))
        window.blit(killed_dead, (10,70))#Смерти (почти как Кира)


        display.update()

    display.update()
    clock.tick(fps)#счетчик фиписи

