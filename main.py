import pygame
import time
from grid import grid_quadry_tree
from setting import *
from ball import ball
import random
import opensimplex
import math
from tools import *
pygame.init()
RUN = True

opensimplex.seed(random.randrange(0, 10000000))

WIDTH = game_setting["width"]
HEIGHT = game_setting["height"]

class Game:
    def __init__(self) -> None:
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(game_setting["title"])


        self.grid_head = self.make_grid()
        self.balls = self.make_balls()


        self.filter = pygame.surface.Surface((WIDTH, HEIGHT))
        self.filter.fill((0, 0, 0))
        self.filter.set_alpha(5)
        self.filter_frame = 1
        self.filter_index = 0
    
    def calc_depth(self):
        grid_depth = 1
        # depth is the number of layers
        win_size = max(WIDTH, HEIGHT)
        while True:
            if win_size <= vector_block_setting["block_size"]:
                break
            else:
                grid_depth += 1
                win_size = win_size//2
        return grid_depth

    def make_sub_grid(self, ls):
        ls2 = []
        for block in ls:
            x1, y1 = block.rect.x,  block.rect.y
            x2, y2 = block.rect.x + block.size//2, block.rect.y + 0
            x3, y3 = block.rect.x + 0, block.rect.y + block.size//2
            x4, y4 = block.rect.x + block.size//2, block.rect.y + block.size//2
            a = grid_quadry_tree((x1, y1), block.size//2)
            ls2.append(a)
            block.top_left = a
            a = grid_quadry_tree((x2, y2), block.size//2)
            ls2.append(a)
            block.top_right = a
            a = grid_quadry_tree((x3, y3), block.size//2)
            ls2.append(a)
            block.bottom_left = a
            a = grid_quadry_tree((x4, y4), block.size//2)
            ls2.append(a)
            block.bottom_right = a
        return ls2

    def make_grid(self):
        self.grid_depth = self.calc_depth()
        size = max(WIDTH, HEIGHT)
        self.grid_tree_head = grid_quadry_tree((0, 0), size)
        sub_grid_todo_list = [self.grid_tree_head]
        for i in range(self.grid_depth - 1):
            sub_grid_todo_list = self.make_sub_grid(sub_grid_todo_list)
        self.set_vectors(sub_grid_todo_list)
        return self.grid_tree_head
    
    def set_vectors(self, ls):
        f = noise_setting["frequency"]
        for block in ls:

            angle = opensimplex.noise2(block.rect.center[0] * f, block.rect.center[1] * f)

            x = math.cos(angle * math.pi)
            y = math.sin(angle * math.pi)

            position = block.center

            direction = pygame.math.Vector2(x, y)
            direction.scale_to_length(ball_setting["maxforce"])

            block.set_vector(position, direction)

    def make_balls(self):
        number = ball_setting["number"]
        balls = []
        for i in range(number):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            balls.append(ball(x, y))
        
        return balls



    def run(self, deltatime):

        for ball in self.balls:
            ball.follow(self.grid_head)
            ball.update(deltatime)
            ball.show(self.WIN)
        

        if self.filter_index >= self.filter_frame:
            self.filter_index = 0
            self.WIN.blit(self.filter, (0, 0))
        else:
            self.filter_index += 1

        pygame.display.update()

def events(events):
    global RUN
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            RUN = False

ex_time = time.time()

game = Game()

while RUN:
    events(pygame.event.get())

    # deltatime
    deltaTime = time.time() - ex_time
    ex_time = time.time()

    game.run(deltaTime)