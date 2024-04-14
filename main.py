from pygame import *
mixer.init()
font.init()

WIDTH, HEIGHT = 500, 600
FPS = 60
display.set_caption('Доганялки')
clock = time.Clock() #game timer

# bg = image.load("background.jpg")
# bg = transform.scale(bg, (WIDTH, HEIGHT)) #resize bg

window = display.set_mode((WIDTH, HEIGHT))
player_img = image.load("images/PLAYER.png")
spike_img = image.load('images/spike.png')
booster1_img = image.load('images/Booster1.png')
oneplate_img = image.load('images/one-plate.png')


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
        sprites.add(self)
    def draw(self, window):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    
    def __init__(self, sprite_image, width=35, height=35, x=100, y=250):
        super().__init__(sprite_image,width, height, x, y)
        self.points = 0
        self.jump = False

    def update(self):
        collidelist = sprite.spritecollide(self, plates, False, sprite.collide_mask)
        if len(collidelist) > 0:
            self.jump = True



plates = sprite.Group()
class Plate(GameSprite):
    def __init__(self, sprite_image, width=45, height=45, x=100, y=250):
        super().__init__(sprite_image, width, height, x, y)
        self.add(plates)
        self.add(sprites)


player = Player(player_img)
oneplate = Plate(oneplate_img)


while True:

    for e in event.get():
        if e.type == QUIT:
            quit()

    if player.jump == True:
        for sprite in sprites:
            sprite.rect.y += 1
        player.jump = False
    
    window.fill((255, 255, 255))
    player.draw(window)
    player.update()
    sprites.draw(window)
    display.update()
    clock.tick(FPS)