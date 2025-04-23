import pygame as pg
from pygame.math import *
import math
import sys
import time



"""
----------------------------------------------------------------------------
Library for better handling of pygame library, with easing everything 
and taking care of many things.
Has its own loop for taking care of things, few funcitons based on godot.
Classes like timer, new sprites for easier work and points of center
                                                            Fizu

                                                            
To add:
+ smooth camera
+ mouse dependant camera
+ rotation from point
+ image groups
+ new image class
+ timer, but time is set in activate, they have func when they finish and/or 
can delete themself
+ timer groups
+ easier text that is also an image
+ something like character node that checks for collision
+ something like enviroment node that has collision but doesnt check for them
+ class for creating worlds

+ whichever funcition shouldnt be used by user should have an underscore

DONE but add more ||| add bliting and updating in handlers in loop, for all sprites and images in group
DONE change rects to frects from community edition
DONE new sprites have init position
DONE add colorkey for sprites
DONE new sprite class, with adding self to group, y sort, center point
DONE local mouse position
DONE clipped camera
DONE global mouse position (include blit size and win size)
DONE new function in sprite and image that tells if local mouse is in them
(add local for hud elements)

LATER:
+ functions for sprites with input that can be changed
animation and audio, also putting these functions in update untouchable



----------------------------------------------------------------------------
"""









"""
Variables for setting everything
"""
#loop init variables
win_size = (1280,720)
blit_size = (960, 540)
scale_w_to_b = Vector2(blit_size[0] / win_size[0], blit_size[1] / win_size[1])
scale_b_to_w = Vector2(win_size[0] / blit_size[0] , win_size[1] / blit_size[1])
game_caption = "Game"
#game_pic = 
game_fps = 60


"""
Groups of sprites and images to blit, update or something
"""
all_timers = []

all_sprites = pg.sprite.Group() #all sprites that are not hud
all_static = pg.sprite.Group() #static, like world
all_dynamic = pg.sprite.Group() #dynamic, like entities
all_images = pg.sprite.Group() #sprites without any collision, working as images
all_hud = pg.sprite.Group() #for sprites on canva, not pushed by camera
all_world = pg.sprite.Group() #for sprites created by ........
#layers
#maybe colliders and collidable
# player, enemies and npcs
# interactable
#





# variables to access, but not to change
camera_off = Vector2(0,0)
camera_tar = Vector2(0,0)

tile_x = 32
tile_y = 32




"""
Usable functions during work, mostly with returns
"""

#getting mouse location on blit screen
def mouse_local_position():
    pos_x, pos_y = pg.mouse.get_pos()
    pos = Vector2(pos_x * scale_w_to_b[0], pos_y * scale_w_to_b[1])
    return pos

def mouse_global_position():
    return camera_off + mouse_local_position()

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
class Sprite(pg.sprite.Sprite):
    def __init__(self, start_pos = (0,0)):
        super().__init__()
        all_sprites.add(self)
        self.layer_blit = 0
        self.colorkey = (0,0,0)
        self.start_pos = start_pos

        #collision
        self.image = pg.Surface((tile_x, tile_y)) #size of collision
        self.image.set_colorkey(self.colorkey)
        self.image.fill((0,0,255))
        self.rect = self.image.get_frect(topleft = self.start_pos) #colision

        #visual
        self.sprite = pg.Surface((tile_x -6, tile_y -6))
        self.sprite.fill((255,255,255))
        self.v_off = Vector2(3,3)

        #variables that always needed to be updated, like center of sprite for camera
        self.center = self.rect.center


        self.init()

    def init(self):
        pass


#TODO later add something about animation

    def update(self):
        pass

    def _update(self, dt):
        self.center = self.rect.center
        self.update()

    def remove(self):
        all_sprites.remove(self)

    
    def mouse_in_rect(self):
        if self.rect.collidepoint(mouse_global_position()):
            return True
        else:
            return False


#from this sprite add:
"""
STATIC BODY
The one that doesnt collide with anything, but is collideable. Probably no movement in them
Like tiles or something
"""
class StaticBody(Sprite):
    def __init__(self, start_pos=(0, 0)):
        super().__init__(start_pos)
        all_static.add(self)

    def remove(self):
        all_sprites.remove(self)
        all_static.remove(self)



"""
DYNAMIC BODY
A one that collides with static bodies.
Like entities or something
"""
class DynamicBody(Sprite):
    def __init__(self, start_pos=(0, 0)):
        super().__init__(start_pos)
        all_dynamic.add(self)

        self.input_vec = Vector2(0,0)
        self.move_vec = Vector2(0,0) #moving the sprite

    #filled by user
    def x_axis_movement(self):
        self.move_vec.x -= 1


    def _x_axis_collision(self):
        for static in all_static.sprites():
            if self.rect.colliderect(static.rect):
                #right
                if self.move_vec.x >0: 
                    self.rect.right = static.rect.left
                #left
                elif self.move_vec.x <0:
                    self.rect.left = static.rect.right
                
                self.move_vec.x = 0

    def _movement_x_axis(self, dt):
        self.rect.centerx += self.move_vec.x * dt


    #filled by user
    def y_axis_movement(self):
        pass
    def _y_axis_collision(self):
        for static in all_static:
            if self.rect.colliderect(static.rect):
                #bottom
                if self.move_vec.y >0:
                    self.rect.bottom = static.rect.top
                #up
                elif self.move_vec.y <0:
                    self.rect.top = static.rect.bottom
                self.move_vec.y = 0

    def _movement_y_axis(self, dt):
        self.rect.centery += self.move_vec.y * dt
    
    def _update(self, dt):
        self.center = self.rect.center
        self.update()

        self.x_axis_movement()
        self._movement_x_axis(dt)
        self._x_axis_collision()
        self.y_axis_movement()
        self._movement_y_axis(dt)
        self._y_axis_collision()

    def remove(self):
        all_sprites.remove(self)
        all_dynamic.remove(self)





class HUD_Sprite(pg.sprite.Sprite):
    def __init__(self, start_pos = (0,0)):
        super().__init__()
        all_hud.add(self)
        self.layer_blit = 0
        self.colorkey = (0,0,0)
        self.start_pos = start_pos

        #collision
        self.image = pg.Surface((tile_x, tile_y)) #size of collision
        self.image.set_colorkey(self.colorkey)
        self.image.fill((0,0,255))
        self.rect = self.image.get_frect(topleft = self.start_pos) #colision

        #visual
        self.sprite = pg.Surface((tile_x - 10, tile_y - 10))
        self.sprite.fill((0,255,0))
        self.v_off = Vector2(5,5)

        #variables that always needed to be updated, like center of sprite for camera
        self.center = self.rect.center


        self.init()

    def init(self):
        pass


#TODO later add something about animation

    def update(self):
        pass

    def _update(self, dt):
        self.center = self.rect.center
        self.update()

    def remove(self):
        all_hud.remove(self)

    
    def mouse_in_rect(self):
        if self.rect.collidepoint(mouse_local_position()):
            return True
        else:
            return False


class Image(pg.sprite.Sprite):
    def __init__(self, start_pos = (0,0)):
        super().__init__()
        all_sprites.add(self)
        all_images.add(self)
        self.layer_blit = 0
        self.colorkey = (0,0,0)
        self.start_pos = start_pos

        #for image
        self.image = pg.Surface((tile_x, tile_y))
        self.image.set_colorkey(self.colorkey)
        self.image.fill((255,0,0))
        self.rect = self.image.get_frect(topleft = self.start_pos)


        #variables that always needed to be updated, like center of sprite for camera
        self.center = self.rect.center


        self.init()

    def init(self):
        pass


#TODO later add something about animation

    def update(self):
        pass

    def _update(self, dt):
        self.center = self.rect.center
        self.update()

    def remove(self):
        all_images.remove(self)
        all_sprites.remove(self)

    
    def mouse_in_rect(self):
        if self.rect.collidepoint(mouse_local_position()):
            return True
        else:
            return False




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



class World():
    def __init__(self):
        pass

    def read_world(self):
        pass
        #return world

    def create_world(self):
        pass

    def destroy_world(self):
        pass

    #some kind of dictonary that would have classes without objects.
    """
    Something like:
    "x012 = Wall
    "kf01 = Door
    """
    
    """
    based on its neighbours it could have a different sprite
    """

    #function io reading that would take a string path and return a world informations, probably json file
    #function that based on the latest function would create a world based on layers and what was needed


    

class Camera():
    def __init__(self):
        self.camera_off = Vector2(0,0)
        self.max_mousedis = 0.4
        self.x = 0
        self.y = 0

    def clipped_movement(self):
        global camera_tar
        self.x, self.y = camera_tar

        self.x = int(self.x - blit_size[0]/2)
        self.y = int(self.y - blit_size[1]/2)
        self.camera_off = Vector2(self.x, self.y)
        global camera_off
        camera_off = self.camera_off

    #smooth TODO

    #mouse based TODO
    
    def display(self, blit_screen):
        l_sprites = all_sprites.sprites()
        l_sprites.sort(key = lambda layer: layer.layer_blit)
        for sprite in l_sprites:
            #collisions
            blit_screen.blit(sprite.image, sprite.rect.topleft - camera_off)
            #images
            blit_screen.blit(\
                sprite.sprite, sprite.rect.topleft + sprite.v_off - camera_off)
        for huds in all_hud:
            blit_screen.blit(huds.sprite, huds.rect.topleft + huds.v_off)

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

        self.next_time = time.time()
        self.dt = 0

        self.camera = Camera()
        self.camera_tar = Vector2(0,0)

        self.init()




    def init(self):
        pass
#for user to use functions
    def input(self):
        pass
    

    def update(self):
        pass

    def display(self):
        pass

#once set functions that shouldnt be modified
    def input_handler(self):
        self.input()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def update_handler(self, dt):
        for timer in all_timers:
            timer.update()
        self.update_sprites(dt)

        self.update()


    def display_handler(self):
        self.screen.fill((0,0,0))
        self.blit_screen.fill((0,0,0))
        self.camera.display(self.blit_screen)

        self.display()

        self.screen.blit(pg.transform.scale(self.blit_screen, win_size), (0,0))


#the funciton with a loop that updates everything
#shouldnt be modified by user
    def loop(self):
        while True:
            self.dt = time.time() - self.next_time
            self.next_time = time.time()

            self.input_handler()
            self.update_handler(self.dt)
            self.display_handler()

            pg.display.flip()
            self.clock.tick(game_fps)
    
    def update_sprites(self, dt):
        for sprite in all_sprites:
            sprite._update(dt)