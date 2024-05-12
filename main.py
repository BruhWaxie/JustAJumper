from pygame import *
from random import *
import pickle
mixer.init()
font.init()

WIDTH, HEIGHT = 500, 600
TILESIZE = 30
FPS = 60
display.set_caption('Go Up')
clock = time.Clock() #game timer
font1 = font.Font('minecraft_font.ttf')

# bg = image.load("background.jpg")
# bg = transform.scale(bg, (WIDTH, HEIGHT)) #resize bg
window = display.set_mode((WIDTH, HEIGHT))

lose_text_img = image.load('loose_title.png')
player_img = image.load("player.png")
playerR_img = image.load('player_r.png')
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
ghost_img = image.load('ghost.png')
logo_img = image.load('GameTitle.png')

max_points = 0


start_text = font1.render('Press SPACE to start the game', True, (122, 122, 122))
restart_text = font1.render('Press SPACE to play again', True, (122, 122, 122))

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
    def set_trpsy(self, alpha):
        self.image.set_alpha(alpha)

class Player(GameSprite):
    def __init__(self, sprite_image, width=35, height=35, x=100, y=250):
        super().__init__(sprite_image,width, height, x, y)
        self.points = 0
        self.jump = False
        self.speed_x = 5
        self.jumpHeight = 0
        self.onground = True
        self.speed_y = 0

    def update(self):
        global p_img, player_img, playerR_img
        self.old_pos = self.rect.x, self.rect.y
        self.oldx = self.rect.x
        keys = key.get_pressed()
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed_x
            self.image = player_img
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed_x
            self.image = playerR_img
        self.image = transform.scale(self.image, (40,40))
        
        if not self.onground:
            self.speed_y += 0.5
            self.rect.y += self.speed_y

        collidelist = sprite.spritecollide(self, plates, False)
        for plate in collidelist:
                self.jumpHeight = plate.power*10
                self.rect.bottom = plate.rect.top
                self.speed_y = 0
                self.onground = True
        if len(collidelist) == 0:
            self.onground = False
        if self.onground:
            self.jump = True
            self.onground = False
            self.speed_y = -self.jumpHeight

        

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
oneplate = Plate(oneplate_img,1, TILESIZE+25, TILESIZE, 225, 425)
height = 0
def generate_map():
    global height
    a = ['p1.txt', 'p2.txt', 'p3.txt', 'p4.txt', 'p5.txt', 'p6.txt', 'p7.txt', 'p8.txt', 'p9.txt', 'p10.txt']
    b = choice(a)
    with open(b, 'r') as file:

        x, y = 0, height
        map = file.readlines()
        for row in map:
            for symbol in row:
                if symbol == 'p':
                    Plate(oneplate_img, 1, TILESIZE, TILESIZE, x,y)
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
                x+=TILESIZE
            y+=TILESIZE
            x=0
def save_best():
    with open('points.dat', 'wb') as file:
        pickle.dump(best_score, file)

lose_text = GameSprite(lose_text_img, 180, 190, 160, 160)
logo = GameSprite(logo_img, 180, 190, 160, 60)
g = GameSprite(ghost_img, 35,35,0,600)
transparency = 255
current_map_top = 0
started = False    
finish = False
start_time = time.get_ticks()
total_time = 0
total_time_text = font1.render(f'Score: {total_time}', True, (122, 122, 122))
best_score = 0
with open('points.dat', 'rb') as file:
    best_score = pickle.load(file)
best_score_text =  font1.render(f'Best Score: {best_score}', True, (122,122,122))



while True:

    for e in event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and finish:  # Restart the game if space is pressed and the game is finished
                finish = False
                sprites.empty()  # Clear all sprites
                current_map_top = 0
                height = 0
                oneplate = Plate(oneplate_img,1, TILESIZE+25, TILESIZE, 225, 425)
                player = Player(player_img, 35, 35, 225, 400)  # Reinitialize player
                generate_map()  # Generate new map
                height = -HEIGHT/2
                g.rect.y = 600
                g.set_trpsy(255)
                transparency = 255
            elif e.key == K_SPACE and not started:
                generate_map()
                height = -HEIGHT/2
                current_map_top = 0
                started = True
    if started and logo.rect.y > -200:
        logo.rect.y -= 5

                         
    if not finish and started:
        player.update()

        if player.jump == True:
            if player.jumpHeight > 0:
                for i in sprites:
                    i.rect.y += 2
                current_map_top += 2
        if current_map_top > 0:
            generate_map()
            current_map_top = -HEIGHT/2
        if player.rect.y >= 600:
            finish = True
            now = time.get_ticks()
            total_time = now - start_time
            total_time_text = font1.render(f'Score: {total_time}', True, (122, 122, 122))
            if best_score < total_time:
                best_score = total_time
            best_score_text =  font1.render(f'Best Score: {best_score}', True, (122,122,122))
            save_best()
            lose_text.draw(window)
            for a in sprites:
                a.kill()
            
    window.fill((255, 255, 255))
    player.draw(window)
    if finish:
        lose_text.draw(window)
        g.rect.x = player.oldx
        g.rect.y -= 1
        if g.rect.y <= 570:
            transparency -= 3
            g.set_trpsy(transparency)
        g.draw(window)

        window.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, 550))
        window.blit(total_time_text, (WIDTH/2 - total_time_text.get_width()/2, 350))
        window.blit(best_score_text, (WIDTH/2 - best_score_text.get_width()/2, 380))
    sprites.draw(window)
    if logo.rect.y > -200:
        logo.draw(window)
    if not started:
        window.blit(start_text, (WIDTH/2 - start_text.get_width()/2, 550))
    display.update()
    clock.tick(FPS)