from pygame import *
from random import *
mixer.init()
font.init()

WIDTH, HEIGHT = 500, 600
TILESIZE = 30
FPS = 60
display.set_caption('Go Up')
clock = time.Clock() #game timer
font1 = font.Font('minecraft_font.ttf')
start_text = 'Press "D" or "A" to start the game'
# bg = image.load("background.jpg")
# bg = transform.scale(bg, (WIDTH, HEIGHT)) #resize bg

window = display.set_mode((WIDTH, HEIGHT))
player_img = image.load("PLAYER.png")
spike_img = image.load('spike.png')
flip_spike_img = transform.flip(spike_img, False, True)
booster1_img = image.load('Booster1.png')
oneplate_img = image.load('one-plate.png')
jumppad1_img = image.load('jumppad1.png')
plate1_img = image.load('plate1.png')
plate2_img = image.load('plate2.png')
plate3_img = image.load('plate3.png')
jumppad1_2variant_img = image.load('jumppad1_2variant.png')
jumppad1_act_img = image.load('jumppad1_activated.png')
booster1_img = image.load('Booster1.png')



sprites = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width=30, height=30, x=100, y=250):
        super().__init__()
        self.hp = 100
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
    def draw(self, window):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    
    def __init__(self, sprite_image, width=35, height=35, x=100, y=250):
        super().__init__(sprite_image,width, height, x, y)
        self.points = 0
        self.jump = False
        self.speed = 5
        self.jumpHeight = 0

    def update(self):
        self.old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        collidelist = sprite.spritecollide(self, plates, False)
        for plate in collidelist:

                self.jumpHeight = plate.power*100
                self.jump = True
        

spikes = sprite.Group()
class Spike(GameSprite):
    def __init__(self, sprite_image, width=45, height=45, x=100, y=250):
        super().__init__(sprite_image, width, height, x, y)
        spikes.add(self)
        sprites.add(self)


plates = sprite.Group()
class Plate(GameSprite):
    def __init__(self, sprite_image,power, width=45, height=45, x=100, y=250):
        super().__init__(sprite_image, width, height, x, y)
        plates.add(self)
        sprites.add(self)
        self.power = power




player = Player(player_img, 35,35, 225, 400)
oneplate = Plate(oneplate_img, TILESIZE, TILESIZE, 225, 400)

def generate_map():
    a = ['p1.txt', 'p2.txt', 'p3.txt', 'p4.txt', 'p5.txt', 'p6.txt', 'p7.txt', 'p8.txt', 'p9.txt', 'p10.txt']
    b = choice(a)
    with open(b, 'r') as file:
        x, y = 0, 0
        map = file.readlines()
        for row in map:
            for symbol in row:
                if symbol == 'p':
                    Plate(oneplate_img, 1, TILESIZE, TILESIZE, x,y)
                elif symbol == 'S':
                    GameSprite(spike_img, TILESIZE, TILESIZE, x,y)
                elif symbol == 'j':
                    Plate(jumppad1_img, 2, TILESIZE,TILESIZE, x,y)
                elif symbol == 'J':
                    Plate(jumppad1_img, 3, TILESIZE,TILESIZE, x,y)
                elif symbol == 'b':
                    GameSprite(booster1_img, TILESIZE,TILESIZE,x,y)
                elif symbol == '1':
                    Plate(plate3_img, 1,TILESIZE,TILESIZE,x,y)
                elif symbol == '2':
                    Plate(plate2_img, 1, TILESIZE,TILESIZE,x,y)
                elif symbol == '3':
                    Plate(plate1_img, 1,TILESIZE,TILESIZE,x,y)
                elif symbol == 's':
                    GameSprite(flip_spike_img, TILESIZE,TILESIZE,x,y-20)
                x+=TILESIZE
            y+=TILESIZE
            x=0

generate_map()


    

while True:

    for e in event.get():
        if e.type == QUIT:
            quit()

    if player.jump == True:
        if player.jumpHeight > 0:
            player.jumpHeight -= 2
            for i in sprites:
               i.rect.y += 2

        player.jump = False
    
    window.fill((255, 255, 255))
    player.draw(window)
    player.update()
    sprites.draw(window)
    display.update()
    clock.tick(FPS)