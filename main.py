import pygame
import sys
import random
import ctypes

# Screen Optimisation ( DPI Awarness)
try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

# --- INITIALISATION ---
pygame.init()
pygame.mixer.init()

# --- SCREEN SETINGS ---
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders - v0.2")

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

# Object
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

# Star System (Parallax)
stars = []
for _ in range(150):
    stars.append([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.uniform(0.5, 3.5)])

# --- FUNCTIONS ---

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def spawn_enemies():
    global enemies
    enemies.clear()
    gap_x, gap_y = 135, 100
    total_cols, total_rows = 15, 6
    start_x = (SCREEN_WIDTH - (total_cols * gap_x)) // 2
    for row in range(total_rows):
        for col in range(total_cols):
            enemy_x = start_x + col * gap_x
            enemy_y = 100 + row * gap_y
            enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

def reset_game():
    global score_value, lives, current_level, enemy_speed_x, enemy_bullet_speed, enemy_direction
    score_value = 0
    lives = 3
    current_level = 1
    enemy_speed_x = 4
    enemy_bullet_speed = 7
    enemy_direction = 1
    invulnerability_duration = 2000
    bullets.clear()
    enemy_bullets.clear()
    spawn_enemies()

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
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

def show_ui():
    draw_text(f"SCORE: {score_value}", score_font, (255, 255, 255), 160, 50)
    draw_text(f"BEST: {high_score}", score_font, (255, 215, 0), 160, 100)
    draw_text(f"LIVES: {lives}", score_font, (255, 0, 0), SCREEN_WIDTH - 160, 50)
    draw_text(f"LEVEL: {current_level}", score_font, (0, 255, 255), SCREEN_WIDTH // 2, 50)

def create_explosion(x, y):
    for _ in range(15):
        particle = {
            'pos' : [x, y],
            'vel' : [random.uniform(-5, 5), random.uniform(-5, 5)],
            'timer' : random.randint(20, 50),
            'color' : (255, random.randint(100, 200), 0)
        }
        particles.append(particle)

# --- MAIN LOOP ---
clock = pygame.time.Clock()

while True:
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bullets.append(pygame.Rect(player_x + player_width//2 - 2, player_y, bullet_width, bullet_height))
                shoot_sound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: save_high_score(score_value); game_state = "MENU"
        
        # Powerups Logic 
        for p in powerups[:]:
            p["rect"].y += 4

            color = (0, 200, 255) if p["type"] == "shield" else (255, 50, 50)
            pygame.draw.rect(screen ,color,  p["rect"], border_radius = 5)

            if p["rect"].colliderect(player_rect):
                if p["type"] == "shield":
                    last_hit_time = pygame.time.get_ticks() + 3500
                elif p["type"] == "life":
                    lives += 1
                powerups.remove(p)
            elif p["rect"].y > SCREEN_HEIGHT:
                powerups.remove(p)

        # Enemies Movement
        move_down_now = False
        current_time = pygame.time.get_ticks()
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height) 
        
        for e in enemies:
            e.x += enemy_speed_x * enemy_direction
            
            
            if player_rect.colliderect(e) and (current_time - last_hit_time > invulnerability_duration):
                hit_sound.play()
                lives -= 1
                last_hit_time = current_time
                if lives <= 0:
                    save_high_score(score_value)
                    game_state = "GAME_OVER"
                else:
                    enemies.clear()
                    enemy_bullets.clear()
                    spawn_enemies()
                break 

            if e.right >= SCREEN_WIDTH or e.left <= 0:
                move_down_now = True
        
        if move_down_now:
            enemy_direction *= -1
            for e in enemies:
                e.y += enemy_move_down
            
            if any(e.bottom >= player_y for e in enemies):
                hit_sound.play()
                lives -= 1
                if lives <= 0:
                    save_high_score(score_value)
                    game_state = "GAME_OVER"
                else:
                    enemies.clear()
                    spawn_enemies()

        # Bullets & Collisions
        for b in bullets[:]:
            b.y -= 18
            if b.y < 0: bullets.remove(b)
            for e in enemies[:]:
                if b.colliderect(e):
                    create_explosion(e.centerx, e.centery)

                    #Power Ups Drops
                    if random.random() < 0.1:
                        pu_type = "shield" if random.random() > 0.5 else "life"
                        powerups.append({"rect": pygame.Rect(e.x, e.y, 25, 25), "type": pu_type})

                    enemies.remove(e)
                    score_value += 10
                    hit_sound.play()
                    if b in bullets:
                        bullets.remove(b)

        # Enemy bullets
        if enemies and random.randint(0, 40) == 1:
            shopper = random.choice(enemies)
            enemy_bullets.append(pygame.Rect(shopper.centerx, shopper.bottom, 6, 18))
        
        for eb in enemy_bullets[:]:
            eb.y += enemy_bullet_speed

            if eb.colliderect(player_rect) and (current_time - last_hit_time > invulnerability_duration):
                lives -= 1
                last_hit_time = current_time
                enemy_bullets.remove(eb)
                hit_sound.play()
                if lives <= 0:
                    save_high_score(score_value)
                    game_state = "GAME_OVER"
            
            elif eb.colliderect(player_rect):
                enemy_bullets.remove(eb)
            
            elif eb.y > SCREEN_HEIGHT:
                enemy_bullets.remove(eb)

        # Draw Stars
        for s in stars:
            s[1] += s[2]
            if s[1] > SCREEN_HEIGHT: s[1] = 0; s[0] = random.randint(0, SCREEN_WIDTH)
            pygame.draw.circle(screen, (255, 255, 255), (int(s[0]), int(s[1])), 2)

        # Draw Explosion Particles
        for p in particles[:]:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["timer"] -= 1

            if p["timer"] <= 0:
                particles.remove(p)
            else:
                pygame.draw.rect(screen, p['color'], (p["pos"][0], p["pos"][1], 4, 4))

        # Draw Objects
        is_invulnerable = (current_time - last_hit_time < invulnerability_duration)


        if is_invulnerable:
            if (current_time // 150) % 2 == 0:
                screen.blit(player_img, (player_x, player_y))
        else:
            screen.blit(player_img, (player_x, player_y))
        
        
        for e in enemies: screen.blit(enemy_img, (e.x, e.y))
        for b in bullets: pygame.draw.rect(screen, (255, 255, 0), b)
        for eb in enemy_bullets: pygame.draw.rect(screen, (200, 50, 50), eb)
        show_ui()

        # Level Up Check
        if len(enemies) == 0:
            current_level += 1
            game_state = "LEVEL_UP"
            level_transition_time = pygame.time.get_ticks()
            invulnerability_duration = 2000
            enemy_speed_x += 1.2
            enemy_bullet_speed += 0.8
            bullets.clear(); enemy_bullets.clear()

    elif game_state == "LEVEL_UP":
        pygame.mouse.set_visible(True)
        draw_scrolling_background(bg_scroll_speed) 
        draw_text(f"LEVEL {current_level}", title_font, (0, 255, 255), SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text("GET READY, CAPTAIN!", button_font, (255, 255, 255), SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120)
        
        if pygame.time.get_ticks() - level_transition_time > 2000:
            spawn_enemies()
            game_state = "GAME"
    
    elif game_state == "GAME_OVER":
        pygame.mouse.set_visible(True)
        screen.fill((0, 0, 0))

        draw_text("MISSION FAILED", title_font, (255, 0, 0), SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
        draw_text(f"FINAL SCORE: {score_value}", button_font, (255, 255, 255), SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text("PRESS 'R' TO RESTART OR 'M' FOR MENU", score_font, (0, 255, 0), SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "GAME"
                if event.key  == pygame.K_m:
                    reset_game()
                    game_state = "MENU"
                
    

    pygame.display.flip()
    clock.tick(60)