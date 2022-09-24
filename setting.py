import pygame

game_setting = {
    "width": 1000,
    "height": 1000,
    "title": "Game",
    'alpha': 200
}


block_number = 64
vector_block_setting = {
    "block_number": block_number,
    "block_size": max(game_setting["width"], game_setting["height"]) // block_number
}

ball_setting = {
    "number": 2000,
    "size": 1,
    "maxspeed": 100,
    "maxforce": 1500
}

noise_setting = {
    "frequency": 0.004
}