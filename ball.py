import pygame
import random
from setting import *

class ball:
    def __init__(self, x, y) -> None:
        self.image = pygame.surface.Surface((ball_setting["size"], ball_setting["size"]))

        self.acc = pygame.math.Vector2(0, 0)
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y)

        self.maxforce = ball_setting["maxforce"]
        self.maxspeed = ball_setting["maxspeed"]

        self.rect = self.image.get_rect(topleft = self.pos)
    
    def update(self, dt):

        self.last_point = self.rect.center
        
        # limiting and applying
        if self.acc.magnitude() > self.maxforce: self.acc.scale_to_length(self.maxforce)
        self.vel += (self.acc * dt)
        
        if self.vel.magnitude() > self.maxspeed: self.vel.scale_to_length(self.maxspeed)
        self.pos += (self.vel * dt)

        # edge teleport
        if self.pos.x < 0: self.pos.x = game_setting["width"]
        if self.pos.x > game_setting["width"]: self.pos.x = 0
        if self.pos.y < 0: self.pos.y = game_setting["height"]
        if self.pos.y > game_setting["height"]: self.pos.y = 0

        # setting the possition
        self.rect.center = self.pos
    
    def show(self, win):
        x = self.last_point[0] - self.rect.center[0]
        y = self.last_point[1] - self.rect.center[1]
        distance = pygame.math.Vector2(x, y)
        if distance.magnitude() < 20:
            pygame.draw.line(win, (200, 0, 200), self.last_point, self.rect.center)
    
    def follow(self, head):
        sub = head
        run = True
        while run:
            if sub.top_left.vector != None:
                run = False

            diff = 1000000000000
            n1 = pygame.math.Vector2(sub.top_left.center[0], sub.top_left.center[1])
            if (n1-self.rect.center).magnitude() < diff: 
                diff = (n1-self.rect.center).magnitude()
                temp = sub.top_left
            n2 = pygame.math.Vector2(sub.top_right.center[0], sub.top_right.center[1])
            if (n2-self.rect.center).magnitude() < diff: 
                diff = (n2-self.rect.center).magnitude()
                temp = sub.top_right
            n3 = pygame.math.Vector2(sub.bottom_left.center[0], sub.bottom_left.center[1])
            if (n3-self.rect.center).magnitude() < diff: 
                diff = (n3-self.rect.center).magnitude()
                temp = sub.bottom_left
            n4 = pygame.math.Vector2(sub.bottom_right.center[0], sub.bottom_right.center[1])
            if (n4-self.rect.center).magnitude() < diff: 
                diff = (n4-self.rect.center).magnitude()
                temp = sub.bottom_right
            diff_block = temp

            sub = diff_block
        self.acc = sub.vector["dir"]
        self.acc.scale_to_length(self.maxforce)