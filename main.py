import pygame
import sys
import random
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

#INIT
pygame.init()
pygame.mixer.init()

#SOUNDS
pygame.mixer.music.load('background-music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound('laser.wav')
hit_sound = pygame.mixer.Sound('explosion.wav')
shoot_sound.set_volume(0.3)
hit_sound.set_volume(0.5)

#SCREEN SETTINGS
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders - Full HD Edition")

#FONT
title_font = pygame.font.Font("GrcafonRegular-8O1nn.otf", 120)
button_font = pygame.font.Font("GrcafonRegular-8O1nn.otf", 50)
score_font = pygame.font.Font("GrcafonRegular-8O1nn.otf", 40)

#IMAGES IMPORT
player_img = pygame.transform.scale(pygame.image.load('ship.png'), (100, 80))
enemy_img = pygame.transform.scale(pygame.image.load('enemy.png'), (80, 60))
background_img = pygame.image.load('background.png')

#STATE
game_state = "MENU"

score_value = 0
lives = 3
font = score_font


def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def reset_game():
    global player_x, player_y, enemies, bullets, score_value, enemy_direction, lives
    
    player_x = (SCREEN_WIDTH / 2) - (player_width / 2)
    player_y = SCREEN_HEIGHT - 150 
    
    lives = 3
    score_value = 0
    bullets.clear()
    enemies.clear()
    enemy_direction = 1
    
    for row in range(6):
        for col in range(14):
            gap_x = 110
            gap_y = 80
            start_x = (SCREEN_WIDTH - (14 * gap_x)) // 2
            
            enemy_x = start_x + col * gap_x
            enemy_y = 150 + row * gap_y
            enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            content = f.read().strip() 
            if content:
                return int(content)
            else:
                return 0
    except (FileNotFoundError, ValueError):
        return 0

high_score = load_high_score()

def save_high_score(new_score):
    global high_score
    if new_score > high_score:
        high_score = new_score 
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

def main_menu():
    global game_state
    pygame.mouse.set_visible(True)
    screen.fill((0, 0, 0))

    #TITLE
    draw_text("SPACE INVADERS", title_font, (0, 255, 0), SCREEN_WIDTH//2, SCREEN_HEIGHT//3)

    #INSTRUCTIONS
    draw_text("PRESS 'ENTER' TO START", button_font, (255, 255, 255), SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)
    draw_text("PRESS 'ESC' TO QUIT", button_font, (200, 200, 200), SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 200)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game() # Reset all
                game_state = "GAME"
            if event.key == pygame.K_ESCAPE: #ESC
                pygame.quit()
                sys.exit()

def show_score(x, y):
    score_txt = font.render(f"SCORE: {score_value}", True, (255, 255, 255))
    screen.blit(score_txt, (x, y))

    high_txt = font.render(f"BEST: {high_score}", True, (255, 215, 0)) # Culoare aurie
    screen.blit(high_txt, (x, y + 50))

    lives_txt = font.render(f"Lives: {lives}", True, (255, 0, 0))
    screen.blit(lives_txt, (SCREEN_WIDTH - 250, y))

#PLAYER DESIGN
player_width = 100
player_height = 50
player_x = (SCREEN_WIDTH / 2) - (player_width / 2)
player_y = SCREEN_HEIGHT - 150
player_speed = 12
player_color = (0, 255, 0)

#BULLETS DESIGN
bullets = []
bullet_speed = 15
bullet_width = 5
bullet_height = 10
bullet_color = (255, 255, 0)
enemy_direction = 1
enemy_move_down = 5 
enemy_speed_x = 4

#ENEMIES DESIGN
enemies = []
enemy_width = 80
enemy_height = 60
enemy_color = (255, 0, 0)
enemy_bullets = []
enemy_bullet_speed = 8
enemy_bullet_color = (139, 0, 0)
#STARS DESIGN
stars = []
for _ in range(100):
    star_x = random.randint(0, SCREEN_WIDTH)
    star_y = random.randint(0, SCREEN_HEIGHT)
    star_speed = random.uniform(0.5, 3.0)
    stars.append([star_x, star_y, star_speed])



for row in range(5):
    for col in range(10):
        enemy_x = 200 + col * 150
        enemy_y = 100 + row * 80
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))





clock = pygame.time.Clock()
running = True
while running:
    #MENU STATE
    if game_state == "MENU":
        main_menu()
    #GAME STATE
    elif game_state == "GAME":
        #MOUSE MOVEMENT
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x = mouse_x - player_width // 2
        player_y = mouse_y - player_height // 2
        pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        new_bullet = pygame.Rect(player_x + player_width//2 - bullet_width//2, player_y, bullet_width, bullet_height)
                        bullets.append(new_bullet)
                        shoot_sound.play()    

            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_ESCAPE:
                    save_high_score(score_value)
                    game_state = "MENU" #Return to MENU
                if event.key == pygame.K_q: #Press "Q" to exit the game instantly
                    pygame.quit()
                    sys.exit()
        #-------------- OLD KEYBOARD MOVEMENT ---------------#
        # keys = pygame.key.get_pressed()
        #PLAYER MOVEMENT LOGIC
        # if keys[pygame.K_LEFT] and player_x > 0:
        #     player_x -= player_speed
            
        # if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        #     player_x += player_speed
        
        # if keys[pygame.K_UP] and player_y > 400:
        #     player_y -= player_speed
        
        # if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_height:
        #     player_y += player_speed
        #-------------- OLD KEYBOARD MOVEMENT ---------------#

        #ENEMY MOVEMENT LOGIC
        move_down_now = False
        for enemy in enemies:
            enemy.x += enemy_speed_x * enemy_direction 
            #Verify if enemies touched the ship
            if enemy.right >= SCREEN_WIDTH or enemy.left <= 0:
                move_down_now = True

        if move_down_now:
            enemy_direction *= -1 #Change direction
            for enemy in enemies:
                enemy.y += enemy_move_down    
            # GAME OVER CHECK
            if any(e.bottom >= player_y for e in enemies):
                lives -= 1
                if lives > 0:
                    bullets.clear()
                    enemy_bullets.clear()
                else:
                    save_high_score(score_value)
                    game_state = "MENU" #TODO : ADD A GAMEOVER gamestate / GAMEOVER screen.
                    pygame.mouse.set_visible(True)

        #ENEMY BULLET LOGIC
        if enemies and random.randint(0, 25) == 1:
            shooter = random.choice(enemies)
            ebullet = pygame.Rect(shooter.centerx, shooter.bottom, 5, 15)
            enemy_bullets.append(ebullet)
        
        for eb in enemy_bullets[:]:
            eb.y += enemy_bullet_speed
            if eb.y > SCREEN_HEIGHT:
                enemy_bullets.remove(eb)
            #COLLISION WITH PLAYER
            if eb.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                hit_sound.play()
                enemy_bullets.remove(eb)
                lives -= 1

                if lives <= 0:
                    save_high_score(score_value)
                    game_state = "MENU"

        #BULLETS LOGIC
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)
                continue
            
            #ENEMIES LOGIC
            for  enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    enemies.remove(enemy)
                    score_value += 10
                    if bullet in bullets:
                        bullets.remove(bullet)

        #DRAWING
        screen.fill((0, 0, 0))
        #STAR MOVEMENT
        for star in stars:
            star[1] += star[2] 
            if star[1] > SCREEN_HEIGHT:
                star[1] = 0
            size = int(star[2] * 0.8) + 1
            pygame.draw.circle(screen, (255, 255, 255), (star[0], int(star[1])), size)

        screen.blit(player_img, (player_x, player_y))

        for enemy in enemies:
            screen.blit(enemy_img, (enemy.x, enemy.y))
        
        for bullet in bullets:
            pygame.draw.rect(screen, bullet_color, bullet)
        
        for ebullet in enemy_bullets:
            pygame.draw.rect(screen, enemy_bullet_color, ebullet)

        show_score(10, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
