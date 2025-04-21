import pygame as pg
import math
import sys



"""
----------------------------------------------------------------------------
Library for better handling of pygame library, with easing everything 
and taking care of many things.
Has its own loop for taking care of things, few funcitons based on godot.
Classes like timer, new sprites for easier work and points of center
                                                            Fizu

                                                            
To add:
+ camera, with camera work. Stuck movement, mouse dependant movement, smooth movement
+ global mouse position (include blit size and win size) and also local position
+ rotation from point
+ image groups
+ new image class
+ new function in sprite and image that tells if local mouse is in them
DONE timer, but time is set in activate, they have func when they finish and/or 
can delete themself
DONE timer groups
+ easier text that is also an image
+ something like character node that checks for collision
+ something like enviroment node that has collision but doesnt check for them

DONE but add more ||| add bliting and updating in handlers in loop, for all sprites and images in group
DONE change rects to frects from community edition
DONE new sprites have init position
DONE add colorkey for sprites
DONE new sprite class, with adding self to group, y sort, center point

LATER:
+ more complex blitting, all sprites are blitted, z and noz, but sorted good. 
+ z sort function for sprites(not in class)
+ sprite groups (all, world etc)

----------------------------------------------------------------------------
"""









"""
Variables for setting everything
"""
#loop init variables
win_size = (1280,720)
blit_size = (960, 540)
scale_w_to_b = (blit_size[0] / win_size[0], blit_size[1] / win_size[1])
scale_b_to_w = (win_size[0] / blit_size[0] , win_size[1] / blit_size[1])
game_caption = "Game"
#game_pic = 
game_fps = 60


"""
Groups of sprites and images to blit, update or something
"""
all_timers = []
sprites_noz = pg.sprite.Group()
#layers
#maybe colliders and collidable
# player, enemies and npcs
# interactable
#


"""
Usable functions during work, mostly with returns
"""

#for clmaping values between two limits
def clamp(value, min_v, max_v):
    return max(min_v, min(value,max_v))


#checking if one key is pressed
def input_pressed(key):
    keys = pg.key_get_pressed()
    if keys[key]:
        return True
    else:
        return False
    
#checking mouse clicks (left, middle, right)
def mouse_pressed(mouse_key):
    mouse_keys = pg.mouse.get_pressed()
    if mouse_keys == mouse_key:
        return True

#moving by some fractions towards the goal
def move_towards(value, delta, finish):
    if value > finish:
        value -= delta
        if value < finish:
            value = finish
    elif value < finish:
        value += delta
        if value > finish:
            value = finish
    return value

#for spliting <Name Sprite (in 1 group)> into "Name Sprite"
def split_spr_name(name):
    sprite = str(name)
    sprite = sprite.split('(')[0]
    sprite = sprite[1:]
    return sprite







"""
Some classes during work. Like basic sprite or image, timer and text on screen
"""
class NewSprite_noZ(pg.sprite.Sprite):
    def __init__(self, start_pos = (0,0)):
        super().__init__()
        sprites_noz.add(self)
        self.layer_blit = 0
        self.colorkey = (0,0,0)
        self.start_pos = start_pos

        self.image = pg.Surface((10,10)) #size of collision
        self.image.set_colorkey(self.colorkey)
        self.rect = self.image.get_frect(topleft = self.start_pos) #colision
    

#TODO later add something about animation

    def update(self):
        pass


#static body

#Timer 
class Timer():
    def __init__(self):
        self.duration = 0
        self.start_time = 0
        self.active = False
        self.current_time = 0
        self.finished = False

        all_timers.append(self)

    def activate(self, duration_ms):
        self.duration = duration_ms
        self.active = True
        self.start_time = pg.time.get_ticks()
    
    def deactivate(self):
        self.active = False
        self.start_time = 0
    
    def update(self):
        self.current_time = pg.time.get_ticks()
        self.finished = False

        if self.active:
            if self.current_time - self.start_time >= self.duration:
                self.finished = True
                self.deactivate()

    def queue_free(self):
        for timer in all_timers:
            if timer is self:
                all_timers.pop(all_timers.index(self))

    




"""
Main class with a game loop inside
"""

class GameLoop():
    def __init__(self):
        pg.init
        self.screen = pg.display.set_mode(win_size)
        self.blit_screen = pg.Surface(blit_size)
        pg.display.set_caption(game_caption)
        self.clock = pg.time.Clock()

        self.player = NewSprite_noZ((100,100))
        self.player.layer_blit = 1
        self.player.image.fill((0,255,0))
        self.plad = NewSprite_noZ((105,105))
        self.plad.image.fill((0,0,255))


        self.init()

    def init(self):
        pass
#for user to use functions
    def input(self):
        pass
    

    def update(self):
        self.update_sprites_noz()

    def display(self):
        self.display_sprites_noz()

#once set functions that shouldnt be modified
    def input_handler(self):
        self.input()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def update_handler(self):
        for timer in all_timers:
            timer.update()
        self.update()


    def display_handler(self):
        self.screen.fill((0,0,0))
        self.blit_screen.fill((0,0,0))
        self.display()
        self.screen.blit(pg.transform.scale(self.blit_screen, win_size), (0,0))


#the funciton with a loop that updates everything
#shouldnt be modified by user
    def loop(self):
        while True:
            self.input_handler()
            self.update_handler()
            self.display_handler()

            pg.display.flip()
            self.clock.tick(game_fps)

    #put this in display()
    def display_sprites_noz(self):
        spritesNoZ = sprites_noz.sprites()
        spritesNoZ.sort(key = lambda layer: layer.layer_blit)
        for sprite in spritesNoZ:
            self.blit_screen.blit(sprite.image, sprite.rect.topleft)
    
    def update_sprites_noz(self):
        for sprite in sprites_noz:
            sprite.update()