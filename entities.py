import pygame
from settings import *
import random
import time


class Boss:
    def __init__(self, image, screen_w, screen_h):
        self.rect = pygame.Rect(screen_w//2 - BOSS_DEFAULT_SIZE[0]//2, 80, BOSS_DEFAULT_SIZE[0], BOSS_DEFAULT_SIZE[1])
        self.hp = BOSS_BASE_HP
        self.max_hp = BOSS_BASE_HP
        self.visible = False
        self.speed_x = BOSS_BASE_SPEED
        self.enraged = False
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.image = image

    def move(self):
        if not self.visible:
            return
        if self.hp < self.max_hp // 2 and not self.enraged:
            self.speed_x *= 1.5
            self.enraged = True
        
        self.rect.x += int(self.speed_x)
        if self.rect.right >= self.screen_w or self.rect.left <= 0:
            self.speed_x *= -1
            
    def draw(self, screen, offset=(0, 0)):
        if not self.visible: return

        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

        bar_width, bar_height, pos_y = 400, 30, 120
        fill_width = int(bar_width * (max(0, self.hp) / self.max_hp))
        bar_x = self.screen_w//2 - bar_width//2 + offset[0]
        bar_y = pos_y + offset[1]

        pygame.draw.rect(screen, (150, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, fill_width, bar_height), 2)


    def shoot(self):
        if not self.visible:
            return []

        new_bullets = []
        if random.randint(0, 30) == 1:
            if not self.enraged:
                new_bullets.append({"rect": pygame.Rect(self.rect.centerx, self.rect.bottom, 10, 25), "vx": 0})
            else:
                new_bullets.append({"rect": pygame.Rect(self.rect.left, self.rect.bottom, 10, 25), "vx": -3}) 
                new_bullets.append({"rect": pygame.Rect(self.rect.centerx, self.rect.bottom, 10, 25), "vx": 0}) 
                new_bullets.append({"rect": pygame.Rect(self.rect.right - 10, self.rect.bottom, 10, 25), "vx": 3})
        return new_bullets


class Enemy:
    def __init__(self, img_list, x, y):
        self.images = img_list
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_timer = pygame.time.get_ticks() + random.randint(0, 500)

    def update_animation(self, current_time):
        if current_time - self.animation_timer > 500:
            self.index = (self.index + 1) % len(self.images)    
            self.image = self.images[self.index]
            self.animation_timer = current_time

    def move(self, speed_x, direction):
        self.rect.x += speed_x * direction
    
    def move_down(self, distance):
        self.rect.y += distance
    
    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))


class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.lives = 3
        self.score = 0
        self.is_invulnerable = False
        self.last_hit_time = 0
        self.weapon_level = 1
        self.credits = 0
    
    def update(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.rect.centerx = m_x
        self.rect.centery = m_y

    def take_damage(self, current_time):
        if current_time - self.last_hit_time > 2000:
            self.lives -= 1
            self.last_hit_time = current_time
            return True
        return False
    
    def draw(self, screen, current_time, offset=(0, 0)):
        is_shielded = current_time - self.last_hit_time < 2000 
        draw_pos = (self.rect.x + offset[0], self.rect.y + offset[1])
        
        if is_shielded:
            shield_center = (self.rect.centerx + offset[0], self.rect.centery + offset[1])
            # pygame.draw.circle(screen, (0, 191, 255), shield_center, 60, 3)
            
            if (current_time // 100) % 2 == 0:
                screen.blit(self.image, draw_pos)
        else:
            screen.blit(self.image, draw_pos)


class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = type
        self.speed_y = 3

    def move(self):
        self.rect.y += self.speed_y

    def draw(self, screen, offset=(0, 0)):
        color = GREEN if self.type == "shield" else YELLOW
        draw_center = (self.rect.centerx + offset[0], self.rect.centery + offset[1])
        pygame.draw.circle(screen, color, draw_center, 15)


def spawn_enemies(enemy_imgs, screen_w):
    new_enemies = []
        
    gap_x, gap_y = 100, 80
    total_cols, total_rows = 12, 5
    
    for row in range(total_rows):
        for col in range(total_cols):
            x = col *(ENEMY_SIZE[0] + gap_x) 
            y = row *(ENEMY_SIZE[1] + gap_y)

            new_enemies.append(Enemy(enemy_imgs, x, y))
    return new_enemies