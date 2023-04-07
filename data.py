import pygame
import os

setting_win = {
    "WIDTH": 1200,
    "HEIGHT": 800,
    "FPS": 60,
    "NAME_GAME": "Space Shooter"
}

setting_hero = {
    "WIDTH": 265,
    "HEIGHT": 175,
    "SPEED": 5
}

setting_bot = {
    "WIDTH": 265,
    "HEIGHT": 175,
    "SPEED": 5
}

setting_boss = {
    "WIDTH": 600,
    "HEIGHT": 200,
}

time_list = []
bots_list = []
bots_shots_list =[]
boss_shot_list = []
buff_list = []

abs_path = os.path.abspath(__file__ + "/..") + "\\image\\"

fon_image = pygame.transform.scale(pygame.image.load("./image/fon2.jpg"), (setting_win["WIDTH"], setting_win["HEIGHT"]))
hero_image = pygame.image.load("hero.png")
bot_image = pygame.image.load("enemy.png")
ammo_hero_image = pygame.transform.scale(pygame.image.load("ammo_hero.png"), (10,20))
boss_image = pygame.image.load("boss.png")
heal_buff_image = pygame.image.load("heal_buff.png")
gun_buff_image = pygame.image.load("gun_buff.png")
#hero_list_image = [hero_image, hero_image]