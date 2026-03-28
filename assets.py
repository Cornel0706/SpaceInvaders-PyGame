import pygame
from settings import *

def load_assets():
    assets = {}
    
    #IMAGES
    assets["player_img"] = pygame.transform.scale(pygame.image.load('assets/ship.png'), PLAYER_SIZE)
    assets["enemy_img"] = pygame.transform.scale(pygame.image.load('assets/enemy.png'), ENEMY_SIZE)
    assets["boss_img"] = pygame.transform.scale(pygame.image.load('assets/boss.png'), BOSS_DEFAULT_SIZE)

    #SOUNDS
    assets["shoot_sound"] = pygame.mixer.Sound('assets/laser.wav')
    assets["explosion_sound"] = pygame.mixer.Sound('assets/explosion.wav')
    assets["background_music"] = pygame.mixer.music.load('assets/background-music.mp3')
    


    #FONTS
    assets["title_font"] = pygame.font.Font("assets/GrcafonRegular-8O1nn.otf", 120)
    assets["score_font"] = pygame.font.Font("assets/GrcafonRegular-8O1nn.otf", 30)

    return assets

    
