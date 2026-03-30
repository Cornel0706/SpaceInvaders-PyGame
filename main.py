import pygame
import sys
import random
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

from settings import *
from entities import Player, Boss, spawn_enemies
from utils import draw_text, create_explosion, load_high_score, save_high_score, get_shake_offset, create_engine_particles
from assets import load_assets

# 1. SETUP INITIAL
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Space Invaders Pro")
clock = pygame.time.Clock()

pygame.mixer.set_num_channels(8)
CHANNEL_PLAYER = pygame.mixer.Channel(0)
CHANNEL_EXPLOSION = pygame.mixer.Channel(1)
CHANNEL_BOSS = pygame.mixer.Channel(2)
CHANNEL_POWERUP = pygame.mixer.Channel(3)

# 2. ASSETS & MUZICĂ
assets = load_assets()
assets["background_music"]
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

# 3. STATE & OBIECTE
high_score = load_high_score()
score_value = 0
current_level = 1
game_state = "MENU"
level_start_time = 0
enemy_direction = 1
shake_intensity = 0 
fade_alpha = 255

player = Player(assets["player_img"])
boss = Boss(assets["boss_img"], SCREEN_WIDTH, SCREEN_HEIGHT)
enemies = spawn_enemies(assets["enemy_imgs"], SCREEN_WIDTH)

bullets = []
enemy_bullets = []
particles = []
powerups = []
stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(1, 3)] for _ in range(100)]

def update_stars():
    for star in stars:
        star[1] += star[2]
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)

def draw_stars(off_x=0, off_y=0):
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0] + off_x, star[1] + off_y), 1)

# --- GAME LOOP ---
running = True
while running:
    current_time = pygame.time.get_ticks()
    screen.fill(BLACK)

    
    off_x, off_y = get_shake_offset(shake_intensity)
    if shake_intensity > 0:
        shake_intensity -= 1 

    update_stars()
    draw_stars(off_x, off_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "GAME":
                    game_state = "PAUSE"
                elif game_state == "PAUSE":
                    game_state = "GAME"
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "GAME":
            bullets.append(pygame.Rect(player.rect.centerx - 2, player.rect.top, 5, 15))
            CHANNEL_PLAYER.play(assets["shoot_sound"])

    # --- STATE: MENU ---
    if game_state == "MENU":
        pygame.mouse.set_visible(True)
        draw_text(screen, "SPACE INVADERS", assets["title_font"], WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//3)

        play_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 60)
        quit_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 80, 300, 60)

        m_pos = pygame.mouse.get_pos()
        m_click = pygame.mouse.get_pressed()[0]

        color_play = GREEN if play_btn.collidepoint(m_pos) else WHITE
        color_quit = RED if quit_btn.collidepoint(m_pos) else WHITE

        draw_text(screen, "START MISSION", assets["score_font"], color_play, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)
        draw_text(screen, "ABANDON SHIP", assets["score_font"], color_quit, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 110)

        if m_click and play_btn.collidepoint(m_pos):
            score_value = 0
            current_level = 1
            player.lives = 3
            enemies = spawn_enemies(assets["enemy_imgs"], SCREEN_WIDTH)
            bullets.clear()
            enemy_bullets.clear()
            powerups.clear()
            boss.visible = False
            game_state = "GAME"
            fade_alpha = 255
        elif m_click and quit_btn.collidepoint(m_pos):
            running = False

    # --- STATE: LEVEL_UP ---
    elif game_state == "LEVEL_UP":
        draw_text(screen, f"LEVEL {current_level}", assets["title_font"], YELLOW, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text(screen, "GET READY...", assets["score_font"], WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)
        
        if current_time - level_start_time > 2000:
            enemy_direction = 1
            if current_level % 5 == 0:
                boss.visible = True
                boss.hp = BOSS_BASE_HP + (current_level * 5)
                boss.rect.centerx = SCREEN_WIDTH // 2
            else:
                enemies = spawn_enemies(assets["enemy_imgs"], SCREEN_WIDTH)
            game_state = "GAME"
            fade_alpha = 255

    # --- STATE: GAME ---
    elif game_state == "GAME":
        player.update()
        pygame.mouse.set_visible(False)
        create_engine_particles(particles, player.rect.centerx, player.rect.bottom - 10)

        # Enemies Movement & Logic
        hit_edge = False
        for e in enemies:
            e.move(INITIAL_ENEMY_SPEED + (current_level // 2), enemy_direction)
            e.update_animation(current_time)
            
            if random.randint(0, 1700) == 1: 
                enemy_bullets.append({
                    "rect": pygame.Rect(e.rect.centerx, e.rect.bottom, 8, 20), 
                    "vx": 0 
                })

            if e.rect.right >= SCREEN_WIDTH or e.rect.left <= 0:
                hit_edge = True
        
        if hit_edge:
            enemy_direction *= -1
            for e in enemies: e.move_down(ENEMY_MOVE_DOWN)
        
        # Collision Kamikaze
        for e in enemies[:]:
            if player.rect.colliderect(e.rect):
                if player.take_damage(current_time):
                    shake_intensity = 15
                    assets["explosion_sound"].play()
                    create_explosion(particles, e.rect.centerx, e.rect.centery)
                    enemies.remove(e)

        if boss.visible:
            boss.move()
            enemy_bullets.extend(boss.shoot())
            if boss.hp <= 0:
                shake_intensity = 40 
                boss.visible = False
                level_start_time = current_time
                game_state = "LEVEL_UP" 

        # Player Bullets 
        for b in bullets[:]:
            b.y -= BULLET_SPEED + 5
            if b.bottom < 0: bullets.remove(b)
            else:
                for e in enemies[:]:
                    if b.colliderect(e.rect):
                        shake_intensity = 5 
                        create_explosion(particles, e.rect.centerx, e.rect.centery)
                        enemies.remove(e)
                        if b in bullets: bullets.remove(b)
                        score_value += 10
                        CHANNEL_EXPLOSION.play(assets["explosion_sound"])
                        if random.random() < 0.02:
                            tipo = random.choice(["life", "shield"])
                            powerups.append({"rect": pygame.Rect(e.rect.centerx, e.rect.y, 20, 20), "type": tipo})
                        break
                
                if boss.visible and b.colliderect(boss.rect):
                    boss.hp -= 2
                    shake_intensity = 3 
                    create_explosion(particles, b.x, b.y)
                    if b in bullets: bullets.remove(b)

        # Enemy Bullets
        for eb in enemy_bullets[:]:
            eb["rect"].y += BULLET_SPEED  
            eb["rect"].x += eb["vx"]      
            if eb["rect"].top > SCREEN_HEIGHT: enemy_bullets.remove(eb)
            elif eb["rect"].colliderect(player.rect):
                if player.take_damage(current_time):
                    shake_intensity = 20
                    assets["explosion_sound"].play()
                if eb in enemy_bullets: enemy_bullets.remove(eb)

        # PowerUp Logic
        for pw in powerups[:]:
            pw["rect"].y += 4
            color = GREEN if pw["type"] == "life" else (0, 191, 255) 
            pygame.draw.circle(screen, color, (pw["rect"].centerx + off_x, pw["rect"].centery + off_y), 12)
            pygame.draw.circle(screen, WHITE, (pw["rect"].centerx + off_x, pw["rect"].centery + off_y), 12, 2)

            if pw["rect"].colliderect(player.rect):
                if pw["type"] == "life": player.lives += 1
                elif pw["type"] == "shield":
                    player.last_hit_time = current_time + 3000
                CHANNEL_POWERUP.play(assets["explosion_sound"])
                powerups.remove(pw)
            elif pw["rect"].top > SCREEN_HEIGHT: powerups.remove(pw)

        if len(enemies) == 0 and not boss.visible:
            current_level += 1
            level_start_time = current_time
            game_state = "LEVEL_UP"
            fade_alpha = 255

        # --- DRAWING with SHAKE ---
        player.draw(screen, current_time, offset=(off_x, off_y))
        boss.draw(screen, offset=(off_x, off_y))
        for e in enemies: e.draw(screen, offset=(off_x, off_y))
        
        for b in bullets: 
            pygame.draw.rect(screen, YELLOW, (b.x + off_x, b.y + off_y, b.width, b.height))
        
        for eb in enemy_bullets: 
            r = eb["rect"]
            pygame.draw.rect(screen, RED, (r.x + off_x, r.y + off_y, r.width, r.height))
        
        for p in particles[:]:
            pygame.draw.circle(screen, p['color'], (int(p['pos'][0] + off_x), int(p['pos'][1] + off_y)), 2)
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]
            p['timer'] -= 1
            if p['timer'] <= 0: particles.remove(p)

        draw_text(screen, f"Score: {score_value}", assets["score_font"], WHITE, 100 + off_x, 50 + off_y)
        draw_text(screen, f"Level: {current_level}", assets["score_font"], YELLOW, SCREEN_WIDTH // 2 + off_x, 50 + off_y) 
        draw_text(screen, f"Lives: {player.lives}", assets["score_font"], RED, 100 + off_x, 90 + off_y)

        if player.lives <= 0:
            high_score = save_high_score(score_value, high_score)
            game_state = "MENU"
            player.lives = 3
            score_value = 0
            current_level = 1
            enemies = spawn_enemies(assets["enemy_imgs"], SCREEN_WIDTH)
            bullets.clear()
            enemy_bullets.clear()
            powerups.clear()
            boss.visible = False
    
    # --- STATE: PAUSE ---
    elif game_state == "PAUSE":
        pygame.mouse.set_visible(True)
        player.draw(screen, current_time)
        boss.draw(screen)
        for e in enemies: e.draw(screen)
        for b in bullets: pygame.draw.rect(screen, YELLOW, b)
        for eb in enemy_bullets: pygame.draw.rect(screen, RED, eb["rect"])

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(screen, "PAUSED", assets["title_font"], WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//3)

        resume_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 60)
        back_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 100, 300, 60)

        m_pos = pygame.mouse.get_pos()
        m_click = pygame.mouse.get_pressed()[0]

        c_res = GREEN if resume_btn.collidepoint(m_pos) else WHITE
        c_bak = RED if back_btn.collidepoint(m_pos) else WHITE

        draw_text(screen, "RESUME", assets["score_font"], c_res, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)
        draw_text(screen, "BACK TO MENU", assets["score_font"], c_bak, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 130)

        if m_click:
            if resume_btn.collidepoint(m_pos):
                game_state = "GAME"
                pygame.mouse.set_visible(False)
            elif back_btn.collidepoint(m_pos):
                game_state = "MENU"

    if fade_alpha > 0:
        fade_alpha -= 3
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill(BLACK)
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()