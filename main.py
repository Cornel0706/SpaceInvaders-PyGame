import pygame
import sys
import random
import ctypes

# Screen Optimisation (DPI Awareness)
try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

# --- INITIALISATION ---
pygame.init()
pygame.mixer.init()

# --- SCREEN SETTINGS ---
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders - v0.3 Boss Update")

# --- RESOURCES ---
try:
    pygame.mixer.music.load('background-music.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
except:
    print("Muzica nu a putut fi incarcata.")

shoot_sound = pygame.mixer.Sound('laser.wav')
hit_sound = pygame.mixer.Sound('explosion.wav')
shoot_sound.set_volume(0.3)
hit_sound.set_volume(0.5)

# Fonts
title_font = pygame.font.Font("GrcafonRegular-8O1nn.otf", 120)
button_font = pygame.font.Font("GrcafonRegular-8O1nn.otf", 50)
score_font = pygame.font.Font("GrcafonRegular-8O1nn.otf", 40)

# Images
player_img = pygame.transform.scale(pygame.image.load('ship.png'), (100, 80))
enemy_img = pygame.transform.scale(pygame.image.load('enemy.png'), (80, 60))
background_img = pygame.image.load('background.png')
menu_background = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))



# --- GAME VARIABLES ---
game_state = "MENU"
score_value = 0
lives = 3
current_level = 1
level_transition_time = 0
bg_scroll_y = 0
bg_scroll_speed = 2

# Object dimensions
player_width, player_height = 100, 80
enemy_width, enemy_height = 80, 60
bullet_width, bullet_height = 5, 15

enemies = []
bullets = []
particles = []
enemy_bullets = []
powerups = []
enemy_direction = 1
enemy_speed_x = 4
enemy_move_down = 35
enemy_bullet_speed = 7

last_hit_time = 0
invulnerability_duration = 2500

# Star System
stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.uniform(0.5, 3.5)] for _ in range(150)]

# BOSS DICTIONARY
boss = {
    "rect" : pygame.Rect(SCREEN_WIDTH//2 - 150, 80, 480, 300),
    "hp" : 100,
    "max_hp": 100,
    "visible" : False,
    "speed_x" : 5,
    "enraged" : False
}

try:
    boss_img_raw = pygame.image.load('boss.png').convert_alpha()
    # Scalam imaginea exact la dimensiunile dreptunghiului Boss-ului
    boss_img = pygame.transform.scale(boss_img_raw, (boss["rect"].width, boss["rect"].height))
except:
    # Dacă nu găsește poza, desenează un dreptunghi mov ca placeholder
    boss_img = pygame.Surface((boss["rect"].width, boss["rect"].height))
    boss_img.fill((150, 0, 150))
    print("Imaginea pentru Boss nu a putut fi încărcată. Folosim placeholder.")

# --- FUNCTIONS ---
def boss_hp_bar():
    if boss["visible"]:
        bar_width = 400
        bar_height = 50
        pos_y = 120
        # Folosim max_hp pentru a calcula proportia corect
        fill_width = int((boss["hp"] / boss["max_hp"]) * bar_width)
        pygame.draw.rect(screen, (150, 0, 0), (SCREEN_WIDTH//2 - bar_width//2, pos_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH//2 - bar_width//2, pos_y, fill_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH//2 - bar_width//2, pos_y, bar_width, bar_height), 2)

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def spawn_enemies():
    global enemies
    enemies.clear()
    gap_x, gap_y = 135, 100
    total_cols, total_rows = 12, 5
    start_x = (SCREEN_WIDTH - (total_cols * gap_x)) // 2
    for row in range(total_rows):
        for col in range(total_cols):
            enemies.append(pygame.Rect(start_x + col * gap_x, 150 + row * gap_y, enemy_width, enemy_height))

def spawn_level_content():
    if current_level % 5 == 0:
        boss["visible"] = True
        boss["hp"] = 100 + (current_level * 20)
        boss["max_hp"] = boss["hp"]
        enemies.clear()
    else:
        boss["visible"] = False
        spawn_enemies()

def reset_game():
    global score_value, lives, current_level, enemy_speed_x, enemy_bullet_speed, enemy_direction, invulnerability_duration
    score_value = 0
    lives = 3
    current_level = 1
    enemy_speed_x = 4
    enemy_bullet_speed = 7
    enemy_direction = 1
    invulnerability_duration = 2000
    bullets.clear()
    enemy_bullets.clear()
    powerups.clear()
    particles.clear()
    spawn_level_content()

def draw_scrolling_background(speed):
    global bg_scroll_y
    screen.blit(menu_background, (0, bg_scroll_y))
    screen.blit(menu_background, (0, bg_scroll_y - SCREEN_HEIGHT))
    bg_scroll_y += speed
    if bg_scroll_y >= SCREEN_HEIGHT:
        bg_scroll_y = 0

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            content = f.read().strip()
            return int(content) if content else 0
    except: return 0

high_score = load_high_score()

def save_high_score(new_score):
    global high_score
    if new_score > high_score:
        high_score = new_score
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
        except: pass

def show_ui():
    draw_text(f"SCORE: {score_value}", score_font, (255, 255, 255), 160, 50)
    draw_text(f"BEST: {high_score}", score_font, (255, 215, 0), 160, 100)
    draw_text(f"LIVES: {lives}", score_font, (255, 0, 0), SCREEN_WIDTH - 160, 50)
    draw_text(f"LEVEL: {current_level}", score_font, (0, 255, 255), SCREEN_WIDTH // 2, 50)

def create_explosion(x, y):
    for _ in range(20):
        particles.append({
            'pos' : [x, y],
            'vel' : [random.uniform(-6, 6), random.uniform(-6, 6)],
            'timer' : random.randint(20, 50),
            'color' : (255, random.randint(100, 200), 0)
        })

# --- MAIN LOOP ---
clock = pygame.time.Clock()

while True:
    current_time = pygame.time.get_ticks()
    
    if game_state == "MENU":
        pygame.mouse.set_visible(True)
        draw_scrolling_background(bg_scroll_speed)
        draw_text("SPACE INVADERS", title_font, (0, 255, 0), SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
        start_btn = pygame.Rect(0, 0, 450, 70); start_btn.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)
        quit_btn = pygame.Rect(0, 0, 450, 70); quit_btn.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 220)
        
        m_pos = pygame.mouse.get_pos()
        s_col = (0, 255, 0) if start_btn.collidepoint(m_pos) else (255, 255, 255)
        q_col = (255, 0, 0) if quit_btn.collidepoint(m_pos) else (255, 255, 255)

        draw_text("START GAME", button_font, s_col, start_btn.centerx, start_btn.centery)
        draw_text("QUIT GAME", button_font, q_col, quit_btn.centerx, quit_btn.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.collidepoint(m_pos): reset_game(); game_state = "GAME"
                if quit_btn.collidepoint(m_pos): pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: reset_game(); game_state = "GAME"
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
        
    elif game_state == "GAME":
        pygame.mouse.set_visible(False)
        screen.fill((0, 0, 0)) 
        
        m_x, m_y = pygame.mouse.get_pos()
        player_x = m_x - player_width // 2
        player_y = m_y - player_height // 2
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # 1. Input Management
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bullets.append(pygame.Rect(player_x + player_width//2 - 2, player_y, bullet_width, bullet_height))
                shoot_sound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: save_high_score(score_value); game_state = "MENU"

        # 2. BOSS LOGIC (Movement & Shooting)
        if boss["visible"]:
            if boss["hp"] < boss["max_hp"] * 0.5 and not boss["enraged"]:
                boss["speed_x"] *= 1.5
                boss["enraged"] = True
        
            boss["rect"].x += boss["speed_x"]
            if boss["rect"].right >= SCREEN_WIDTH or boss["rect"].left <= 0:
                boss["speed_x"] *= -1
            
            # Boss Shooting
            if random.randint(0, 30) == 1:
                if not boss["enraged"]:
                    enemy_bullets.append({"rect": pygame.Rect(boss["rect"].centerx, boss["rect"].bottom, 10, 25), "vx": 0})
                else:
                    enemy_bullets.append({"rect": pygame.Rect(boss["rect"].left, boss["rect"].bottom, 10, 25), "vx": -3}) 
                    enemy_bullets.append({"rect": pygame.Rect(boss["rect"].centerx, boss["rect"].bottom, 10, 25), "vx": 0}) 
                    enemy_bullets.append({"rect": pygame.Rect(boss["rect"].right - 10, boss["rect"].bottom, 10, 25), "vx": 3})  

        # 3. Enemy Movement (Standard)
        if not boss["visible"]:
            move_down_now = False
            for e in enemies:
                e.x += enemy_speed_x * enemy_direction
                if e.right >= SCREEN_WIDTH or e.left <= 0: move_down_now = True
                
                # Collision player-enemy
                if player_rect.colliderect(e) and (current_time - last_hit_time > invulnerability_duration):
                    hit_sound.play()
                    lives -= 1
                    last_hit_time = current_time
                    if lives <= 0: save_high_score(score_value); game_state = "GAME_OVER"
                    else: spawn_level_content() # Reset level layout
                    break
            
            if move_down_now:
                enemy_direction *= -1
                for e in enemies: e.y += enemy_move_down

        # 4. Bullets & Collisions
        for b in bullets[:]:
            b.y -= 18
            if b.y < 0: 
                bullets.remove(b)
                continue 
            
            hit_something = False
            
            # Hit Boss
            if boss["visible"] and b.colliderect(boss["rect"]):
                boss["hp"] -= 2
                hit_sound.play()
                bullets.remove(b)
                hit_something = True
                if boss["hp"] <= 0:
                    create_explosion(boss["rect"].centerx, boss["rect"].centery)
                    create_explosion(boss["rect"].left, boss["rect"].top)
                    create_explosion(boss["rect"].right, boss["rect"].bottom)

                    boss["enraged"] = False
                    boss["visible"] = False
                    boss["speed_x"] = 5
            
            # Hit Enemies
            if not hit_something:
                for e in enemies[:]:
                    if b.colliderect(e):
                        create_explosion(e.centerx, e.centery)
                        if random.random() < 0.05:
                            pu_type = "shield" if random.random() > 0.2 else "life" 
                            powerups.append({"rect": pygame.Rect(e.x, e.y, 25, 25), "type": pu_type})
                        enemies.remove(e)
                        score_value += 10
                        hit_sound.play()
                        bullets.remove(b)
                        hit_something = True
                        break

        # 5. Enemy Bullets Logic
        if not boss["visible"] and enemies and random.randint(0, 40) == 1:
            shopper = random.choice(enemies)
            enemy_bullets.append({"rect": pygame.Rect(shopper.centerx, shopper.bottom, 6, 18), "vx": 0})
        
        for eb in enemy_bullets[:]:
            eb["rect"].y += enemy_bullet_speed
            eb["rect"].x += eb["vx"]

            if eb["rect"].colliderect(player_rect):
                if (current_time - last_hit_time > invulnerability_duration):
                    lives -= 1
                    last_hit_time = current_time
                    hit_sound.play()
                    if lives <= 0: save_high_score(score_value); game_state = "GAME_OVER"
                enemy_bullets.remove(eb)
            elif eb["rect"].y > SCREEN_HEIGHT:
                enemy_bullets.remove(eb)

        # 6. Powerups Logic
        for p in powerups[:]:
            p["rect"].y += 4
            color = (0, 200, 255) if p["type"] == "shield" else (255, 50, 50)
            pygame.draw.rect(screen, color, p["rect"], border_radius=15)
            if p["rect"].colliderect(player_rect):
                if p["type"] == "shield": last_hit_time = current_time + 3500
                else: lives += 1
                powerups.remove(p)
            elif p["rect"].y > SCREEN_HEIGHT: powerups.remove(p)

        # 7. DRAWING PHASE
        # Stars
        for s in stars:
            s[1] += s[2]
            if s[1] > SCREEN_HEIGHT: s[1] = 0; s[0] = random.randint(0, SCREEN_WIDTH)
            pygame.draw.circle(screen, (255, 255, 255), (int(s[0]), int(s[1])), 2)

        # Particles
        for p in particles[:]:
            p["pos"][0] += p["vel"][0]; p["pos"][1] += p["vel"][1]; p["timer"] -= 1
            if p["timer"] <= 0: particles.remove(p)
            else: pygame.draw.rect(screen, p['color'], (p["pos"][0], p["pos"][1], 4, 4))

        # Boss
        if boss["visible"]:
            # Scalam imaginea inamicului pentru Boss
            screen.blit(boss_img, (boss["rect"].x, boss["rect"].y))
            boss_hp_bar()

        # Standard Enemies & Bullets
        for e in enemies: screen.blit(enemy_img, (e.x, e.y))
        for b in bullets: pygame.draw.rect(screen, (255, 255, 0), b)
        for eb in enemy_bullets: pygame.draw.rect(screen, (200, 50, 50), eb["rect"])
        
        # Player (Blink if invulnerable)
        is_invulnerable = (current_time - last_hit_time < invulnerability_duration)
        if not is_invulnerable or (current_time // 150) % 2 == 0:
            screen.blit(player_img, (player_x, player_y))
        
        show_ui()

        # 8. Level Transition Logic
        level_finished = False
        if not boss["visible"] and len(enemies) == 0:
            level_finished = True
        elif boss["visible"] and boss["hp"] <= 0:
            create_explosion(boss["rect"].centerx, boss["rect"].centery)
            score_value += 1000
            level_finished = True

        if level_finished:
            current_level += 1
            game_state = "LEVEL_UP"
            level_transition_time = current_time
            bullets.clear()
            enemy_bullets.clear()
            spawn_level_content()

    elif game_state == "LEVEL_UP":
        draw_scrolling_background(bg_scroll_speed) 
        draw_text(f"LEVEL {current_level}", title_font, (0, 255, 255), SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text("GET READY, CAPTAIN!", button_font, (255, 255, 255), SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120)
        if current_time - level_transition_time > 2000:
            game_state = "GAME"
    
    elif game_state == "GAME_OVER":
        screen.fill((0, 0, 0))
        draw_text("MISSION FAILED", title_font, (255, 0, 0), SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
        draw_text(f"FINAL SCORE: {score_value}", button_font, (255, 255, 255), SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text("PRESS 'R' TO RESTART OR 'M' FOR MENU", score_font, (0, 255, 0), SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: reset_game(); game_state = "GAME"
                if event.key == pygame.K_m: reset_game(); game_state = "MENU"

    pygame.display.flip()
    clock.tick(60)