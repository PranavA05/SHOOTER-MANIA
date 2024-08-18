from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state,self.frames_index='down',0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60,-90) # to remove whitespace of player's width

        # movement
        self.direction = pygame.Vector2()
        self.speed = 250
        self.collision_sprites=collision_sprites

    def load_images(self) :
        self.frames={'left':[],'right':[],'up':[],'down':[]}
        for state in self.frames.keys():    
            for folder_path, sub_folders, file_names in walk(join('images','player',state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])): # sorting it in case the files aren't in order | may lead to wonkiness 
                        full_path=join(folder_path,file_name)
                        surf=pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):  
        keys=pygame.key.get_pressed()
        self.direction.x=int(keys[pygame.K_d]-keys[pygame.K_a])
        self.direction.y=int(keys[pygame.K_s]-keys[pygame.K_w])
        self.direction +=self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt # horizontal
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y  * self.speed * dt #vertical
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
                      # Moving down
    def animate(self,dt):
        # get state
        if self.direction.x !=0:
            self.state='right' if self.direction.x > 0 else 'left'
        if self.direction.y !=0:
            self.state='down' if self .direction.y > 0 else 'up'
        #animate
        self.frames_index = self.frames_index + 5 * dt if self.direction else 0
        self.image= self.frames[self.state][int(self.frames_index) % len(self.frames[self.state])]
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)