import pygame
from settings import *
from math import atan2,degrees

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)  # Unpack groups if it's a tuple
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.ground= True
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)  # Unpack groups if it's a tuple
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
class Gun(pygame.sprite.Sprite): # Need to decide whether we want to align the gun according to the offset of all the sprites or assume the plaer as the cemter
    def __init__(self,player,groups):
        self.player=player
        self.distance=140
        self.player_direction = pygame.Vector2(1,0)
        self.gun_direction = self.player_direction
        # sprite setup
        super().__init__(groups)
        self.gun_surf =pygame.image.load(join('images','gun','gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center=self.player.rect.center + self.player_direction * self.distance)
        self.bullet=pygame.image.load(join('images','gun','bullet.png'))
    def get_direction(self):
        mouse_pos=pygame.Vector2(pygame.mouse.get_pos())
        player_pos=pygame.Vector2(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        self.player_direction = (mouse_pos-player_pos).normalize()
    def rotate_gun(self):
        angle=degrees(atan2(self.player_direction.x,self.player_direction.y ))-90
        if self.player_direction.x >0:
            self.image=pygame.transform.rotozoom(self.gun_surf,angle,1) # using image would be wrong as we would want the gun to shoot too so we shall take the surface
        else:
            self.image=pygame.transform.rotozoom(self.gun_surf,abs(angle),1)
            self.image=pygame.transform.flip(self.image,False,True )

    def update(self,dt):
        self.get_direction()
        self.rotate_gun()
        self.rect.center=self.player.rect.center + self.player_direction * self.distance 
class Bullet(pygame.sprite.Sprite):
    def __init__(self,surf,pos,direction,groups):
        super().__init__(groups)
        self.image=surf 
        self.rect=self.image.get_rect(center=pos)
        self.direction= direction
        self.speed =1200

    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt 
class Enemy(pygame.sprite.Sprite):
    def __init__( self,pos,frames,groups,player,collision_sprites):
        super().__init__(groups)
        self.player=player

        # image
        self.frames , self.frame_index=frames,0
        self.image = self.frames[self.frame_index]
        self.animation_speed=6

        self.rect=self.image.get_rect(center=pos)
        self.hitbox_rect=self.rect.inflate(-20,-40)
        self.collision_sprites=collision_sprites
        self.direction=pygame.Vector2()
        self.speed=350

        # timeer
        self.death_time=0
        self.death_duration =400

    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image= self.frames[int(self.frame_index) % len(self.frames)] 
    def move(self, dt):
        player_pos= pygame.Vector2(self.player.rect.center)
        enemy_pos =pygame.Vector2(self.rect.center)
        self.direction=(player_pos-enemy_pos).normalize()
    
        # update the rect position
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        self.rect.center = self.hitbox_rect.center
    def collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction =='horizontal':                            
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left # if x > 0 we going right & we set the self.rect's position to the same as the the obstacles side which it collided with
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0:  self.hitbox_rect.bottom = sprite.rect.top 
                    if self.direction.y < 0:  self.hitbox_rect.top = sprite.rect.bottom  
    def destroy(self):
        # start timer
        self.death_time= pygame.time.get_ticks()
        # change the image
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image= surf
    def death_timer(self):
        if pygame.time.get_ticks() -self.death_time >= self.death_duration:
            self.kill()
    def update(self,dt):
        if self.death_time ==0:

            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()