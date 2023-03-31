#!/usr/bin/env python3

import pygame
import data
import shooter_object as so
import time
import random

pygame.init()

window = pygame.display.set_mode((data.setting_win["WIDTH"], data.setting_win["HEIGHT"]))
pygame.display.set_caption(data.setting_win["NAME_GAME"])
def run():
    game = True
    start_time = 0
    end_time = 0
    lvl = 1
    end_time_botAndShot = 0
    stop_shot = -3000
    start_time_bot = pygame.time.get_ticks()
    font_text = pygame.font.Font(None, 40)
    font_shot_counter = pygame.font.Font(None, 40)

    clock = pygame.time.Clock()
    hero = so.Hero(data.setting_win["WIDTH"] //  2- data.setting_hero["WIDTH"] // 2, data.setting_win["HEIGHT"] - data.setting_hero["HEIGHT"], data.setting_hero["WIDTH"],data.setting_hero["HEIGHT"], data.setting_hero["SPEED"], data.hero_image)
    boss = so.Boss(data.setting_win["WIDTH"] //  2- data.setting_boss["WIDTH"] // 2, -data.setting_boss["HEIGHT"], data.setting_boss["WIDTH"], data.setting_boss["HEIGHT"], 1, data.hero_image)
    #bot = so.Bot(random.randint(0, data.setting_win["WIDTH"] - 50), -100, 150, 100, 1, data.bot_image)
    while game:
        window.blit(data.fon_image, (0,0))

        window.blit(font_text.render(f"HP: {hero.HP}", True, (255,0,0)), (data.setting_win["WIDTH"]-100, 10))

        window.blit(font_text.render(f"HP: {hero.POINT}", True, (0,255,0)), (data.setting_win["WIDTH"]-250, 10))

        window.blit(hero.IMAGE, (hero.x, hero.y))
        #window.blit(bot.IMAGE, (bot.x, bot.y))
        #start_time =time()

        hero.move()
        window.blit(font_shot_counter.render(f"{5 - hero.BULLET_COUNTER}", True, (255,0,0)), (hero.x + hero.width, hero.y))
        # end_time = time()
        # data.time_list.append(end_time - start_time)
        # bot.move()
        number_bullets = 0
        for bullets in hero.BULLETS:
            for bullet in bullets:
                bullet.move_bullet(hero, boss, bullet, who_shot = "hero", number_bullets = number_bullets)
                window.blit(bullet.IMAGE, (bullet.x, bullet.y))
            number_bullets += 1

        for buff in data.buff_list:
            buff.y += 1 
            window.blit(buff.IMAGE, (buff.x, buff.y))
            if buff.colliderect(hero) and buff.BUFF == "heal":
                hero.HP += 1
                data.buff_list.remove(buff)
            if buff.colliderect(hero) and buff.BUFF == "gun":
                hero.GUN = 2
                data.buff_list.remove(buff)

        for bot in data.bots_list:
            window.blit(bot.IMAGE, (bot.x, bot.y))
            bot.move(bot, hero)
            if bot.MAKE_SHOT:
                data.bots_shots_list.append(so.Shot(bot.x + bot.width // 2 - 5, bot.y+bot.height, 10, 20, data.ammo_hero_image, 3, bot = bot))
                bot.MAKE_SHOT = False
            # if not bot.MAKE_SHOT:
            #     bot.SHOT.move_bullet(hero, bot = bot, find_bullet = bot.SHOT)
            #     window.blit(bot.SHOT.IMAGE, (bot.SHOT.x, bot.SHOT.y))
        
        for bullet in data.bots_shots_list:
            window.blit(bullet.IMAGE, (bullet.x, bullet.y))
            bullet.move_bullet(hero, boss, bullet, who_shot = "bot")

        end_time_botAndShot = pygame.time.get_ticks()
        #print(end_time_bot, start_time_bot)
        if end_time_botAndShot - start_time_bot > 2000 and hero.POINT < 100:
            data.bots_list.append(so.Bot(random.randint(0, data.setting_win["WIDTH"] - data.setting_bot["WIDTH"] // 3), data.setting_bot["HEIGHT"], data.setting_bot["WIDTH"], data.setting_bot["HEIGHT"], 1, data.bot_image))
            start_time_bot = end_time_botAndShot
        #BOSS
        if hero.POINT >= 100:
            window.blit(data.boss_image, (boss.x,boss.y))
            boss.move()
            if end_time_botAndShot - start_time_bot > 2000:
                data.boss_shot_list.append( [so.Shot(boss.x + data.setting_boss["WIDTH"] // 2 - 57, boss.y + data.setting_boss["HEIGHT"] - 15, 10, 20, data.ammo_hero_image, 3),
                                            so.Shot(boss.x + data.setting_boss["WIDTH"] // 2 + 57, boss.y + data.setting_boss["HEIGHT"] - 15, 10, 20, data.ammo_hero_image, 3)])
                start_time_bot = end_time_botAndShot
            number_bullets = 0
            for bullets in data.boss_shot_list:
                for bullet in bullets:
                    bullet.move_bullet(hero, boss, bullet, who_shot = "boss", number_bullets = number_bullets)
                    window.blit(bullet.IMAGE, (bullet.x, bullet.y))
                number_bullets += 1
            #boss die
            if boss.HP <= 0:
                hero.POINT += 100
                hero.ALL_POINTS += hero.POINT
                hero.POINT = 0
                window.blit(pygame.font.SysFont("Comic Sans MS", 100, bold = True).render(f"Рівень{lvl}", True, (161, 76, 179)), (data.setting_win["WIDTH"] // 2 - 100, data.setting_win["HEIGHT"] // 2 -50))
                
                pygame.display.flip()
                lvl += 1 
                boss.HP = 10
                boss.x = data.setting_win["WIDTH"] // 2 - data.setting_boss["WIDTH"] // 2
                boss.y = -data.setting_boss["HEIGHT"]
                time.sleep(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero.MOVE["UP"] = True
                if event.key == pygame.K_s:
                    hero.MOVE["DOWN"] = True
                if event.key == pygame.K_a:
                    hero.MOVE["LEFT"] = True
                if event.key == pygame.K_d:
                    hero.MOVE["RIGHT"] = True
                if event.key == pygame.K_SPACE and end_time_botAndShot - stop_shot > 3000:
                    hero.BULLETS.append([so.Shot(hero.x + hero.width // 2 - 37, hero.y, 10, 20, data.ammo_hero_image, -10),
                                        so.Shot(hero.x + hero.width // 2 + 37, hero.y, 10, 20, data.ammo_hero_image, -10)])
                    if hero.GUN == 2:
                        hero.BULLETS.append([so.Shot(hero.x + 20, hero.y + 50, 10, 20, data.ammo_hero_image, -10),
                                            so.Shot(hero.x + hero.width - 20, hero.y + 50, 10, 20, data.ammo_hero_image, -10)])
                    hero.BULLET_COUNTER += 1
                    if hero.BULLET_COUNTER == 5:
                        stop_shot = end_time_botAndShot
                if event.key == pygame.K_r:
                    hero.BULLET_COUNTER =0
                    stop_shot = end_time_botAndShot
                    hero.BULLET_COUNTER = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    hero.MOVE["UP"] = False
                if event.key == pygame.K_s:
                    hero.MOVE["DOWN"] = False
                if event.key == pygame.K_a:
                    hero.MOVE["LEFT"] = False
                if event.key == pygame.K_d:
                    hero.MOVE["RIGHT"] = False

        clock.tick(data.setting_win["FPS"])
        pygame.display.flip()

run()
# for t in data.time_list:
#     a += t
# print(a/len(data.time_list))