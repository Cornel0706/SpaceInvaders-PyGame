import pygame
import random


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def create_explosion(particles_list, x, y):
    for _ in range(20):
        particles_list.append({
            'pos' : [x, y],
            'vel' : [random.uniform(-6, 6), random.uniform(-6, 6)],
            'timer' : random.randint(20, 50),
            'color' : (255, random.randint(100, 200), 0)
        })

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            content = f.read().strip()
            return int(content) if content.isdigit() else 0
    except: return 0

def save_high_score(new_score, current_high_score):
    if new_score > current_high_score:
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(new_score))
            return new_score 
        except: 
            pass
    return current_high_score

def move_stars(stars_list, screen_h, screen_w):
    for star in stars_list:
        star[1] += star[2] 
        if star[1] > screen_h:
            star[1] = 0
            star[0] = random.randint(0, screen_w)

def draw_stars(screen, stars_list):
    for star in stars_list:
        pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), 2)
    

