import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()

# =====================
# SCREEN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# =====================
# PATHS
# =====================
BASE = os.path.dirname(__file__)
ASSETS = os.path.join(BASE, "assets")
IMG = os.path.join(ASSETS, "images")
SND = os.path.join(ASSETS, "sounds")

def img(name, size=None):
    path = os.path.join(IMG, name)
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    s = pygame.Surface(size if size else (50,50))
    s.fill((255,0,0))
    return s

def snd(name):
    path = os.path.join(SND, name)
    return pygame.mixer.Sound(path) if os.path.exists(path) else None

# =====================
# AUDIO
# =====================
shoot_sound = snd("shoot.wav")
explosion_sound = snd("explosion.wav")

music_path = os.path.join(SND, "music.mp3")
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

# =====================
# IMAGES
# =====================
bg = img("background.png", (WIDTH, HEIGHT))
player_img = img("player1.png", (80, 80))
hard_img = img("hard.png", (70, 70))
levelup_img = img("levelup.png", (300, 250))
gameover_img = img("gameover.png", (400, 200))

enemy_imgs = [
    img("enemy1.png", (75,75)),
    img("enemy2.png", (75,75)),
    img("enemy3.png", (75,75)),
    img("enemy4.png", (75,75)),
    img("enemy5.png", (75,75)),
]

boss_img = img("boss.png", (140,140))

# =====================
# BUTTONS
# =====================
def draw_button(text, rect, base, hover):
    color = hover if rect.collidepoint(pygame.mouse.get_pos()) else base
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=12)

    label = font.render(text, True, (255,255,255))
    screen.blit(label, (
        rect.centerx - label.get_width()//2,
        rect.centery - label.get_height()//2
    ))

btn_play = pygame.Rect(300, 220, 200, 70)
btn_exit = pygame.Rect(300, 320, 200, 70)
btn_restart = pygame.Rect(300, 380, 200, 60)
btn_menu = pygame.Rect(300, 460, 200, 60)

# =====================
# GAME STATE
# =====================
menu = True
game_over = False

score = 0
level = 1
levelup_timer = 0

hp = 100
max_hp = 100

player = pygame.Rect(400, 300, 70, 70)
speed = 4

bullets = []
enemies = []
hard = []

boss = None
boss_hp = 0
boss_max_hp = 1200

# =====================
# RESET GAME
# =====================
def reset_game():
    global hp, score, level, enemies, bullets, hard, boss, game_over

    hp = max_hp
    score = 0
    level = 1

    enemies = [spawn_enemy() for _ in range(5)]
    bullets = []
    hard = []

    boss = None
    game_over = False

# =====================
# SPAWN
# =====================
def spawn_enemy():
    return {
        "rect": pygame.Rect(random.randint(0, WIDTH-60),
                            random.randint(0, HEIGHT-60), 60, 60),
        "type": random.randint(0,4)
    }

def spawn_boss():
    global boss_hp
    boss_hp = boss_max_hp + level * 200
    return pygame.Rect(WIDTH//2, 80, 140, 140)

# =====================
# INIT ENEMIES
# =====================
enemies = [spawn_enemy() for _ in range(5)]

# =====================
# LOOP
# =====================
running = True

while running:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()

    # =====================
    # EVENTS
    # =====================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = not menu

            if event.key == pygame.K_SPACE and not menu and not game_over:
                px, py = player.center
                dx, dy = mx - px, my - py
                dist = math.sqrt(dx*dx + dy*dy)
                if dist != 0:
                    dx /= dist
                    dy /= dist
                bullets.append([px, py, dx*10, dy*10])

        # CLICK SYSTEM
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # MENU
            if menu:
                if btn_play.collidepoint(mx,my):
                    menu = False
                    reset_game()

                if btn_exit.collidepoint(mx,my):
                    running = False

            # GAME OVER
            if game_over:
                if btn_restart.collidepoint(mx,my):
                    reset_game()
                    menu = False

                if btn_menu.collidepoint(mx,my):
                    menu = True
                    game_over = False

    # =====================
    # MENU
    # =====================
    if menu:
        screen.fill((20,20,30))
        draw_button("PLAY", btn_play, (40,120,200), (80,160,255))
        draw_button("EXIT", btn_exit, (200,40,40), (255,80,80))
        pygame.display.flip()
        continue

    # =====================
    # GAME OVER
    # =====================
    if hp <= 0:
        game_over = True

    if game_over:
        screen.fill((0,0,0))

        screen.blit(
            gameover_img,
            (WIDTH//2 - gameover_img.get_width()//2,
             HEIGHT//2 - gameover_img.get_height()//2 - 120)
        )

        draw_button("RESTART", btn_restart, (40,200,120), (80,255,160))
        draw_button("MENU", btn_menu, (120,40,200), (160,80,255))

        pygame.display.flip()
        continue

    # =====================
    # LEVEL
    # =====================
    old_level = level
    level = score // 200 + 1

    if level > old_level:
        levelup_timer = 60

    if level % 5 == 0 and boss is None:
        boss = spawn_boss()

    # =====================
    # DRAW BG
    # =====================
    screen.blit(bg,(0,0))

    # =====================
    # MOVE PLAYER
    # =====================
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player.y -= speed
    if keys[pygame.K_s]: player.y += speed
    if keys[pygame.K_a]: player.x -= speed
    if keys[pygame.K_d]: player.x += speed

    player.x = max(0, min(WIDTH-player.width, player.x))
    player.y = max(0, min(HEIGHT-player.height, player.y))

    # =====================
    # BULLETS
    # =====================
    for b in bullets[:]:
        b[0]+=b[2]
        b[1]+=b[3]

    # =====================
    # ENEMIES
    # =====================
    for e in enemies[:]:
        r = e["rect"]

        dx = player.x - r.x
        dy = player.y - r.y
        dist = math.sqrt(dx*dx+dy*dy)

        if dist != 0:
            r.x += dx/dist*(1.5+level*0.2)
            r.y += dy/dist*(1.5+level*0.2)

        if player.colliderect(r):
            hp -= 2
            enemies.remove(e)

    # =====================
    # HARD (APTECHEKA)
    # =====================
    if random.randint(1, 200) == 1:
        hard.append([pygame.Rect(random.randint(50, WIDTH-50),
                                 random.randint(50, HEIGHT-50), 50, 50), 300])

    for h in hard[:]:
        rect = h[0]
        screen.blit(hard_img, rect.topleft)

        h[1] -= 1
        if h[1] <= 0:
            hard.remove(h)
            continue

        if player.colliderect(rect):
            hp += 25
            hp = min(max_hp, hp)
            hard.remove(h)

    # =====================
    # BOSS
    # =====================
    if boss:
        dx = player.centerx - boss.centerx
        dy = player.centery - boss.centery
        dist = math.sqrt(dx*dx+dy*dy)

        if dist != 0:
            boss.x += dx/dist*(1.2+level*0.2)
            boss.y += dy/dist*(1.2+level*0.2)

        if player.colliderect(boss):
            hp -= 3

        hp_ratio = boss_hp / (boss_max_hp + level*200)
        pygame.draw.rect(screen,(80,0,0),(WIDTH//2-100,20,200,15))
        pygame.draw.rect(screen,(255,0,0),(WIDTH//2-100,20,200*hp_ratio,15))

    # =====================
    # COLLISIONS
    # =====================
    for b in bullets[:]:
        for e in enemies[:]:
            if e["rect"].collidepoint(b[0],b[1]):
                enemies.remove(e)
                bullets.remove(b)
                score += 10
                break

        if boss and boss.collidepoint(int(b[0]),int(b[1])):
            boss_hp -= 10
            bullets.remove(b)

            if boss_hp <= 0:
                boss = None
                score += 500

    if len(enemies) < 5:
        enemies.append(spawn_enemy())

    # =====================
    # DRAW
    # =====================
    screen.blit(player_img, player.topleft)

    for e in enemies:
        screen.blit(enemy_imgs[e["type"]], e["rect"].topleft)

    for b in bullets:
        pygame.draw.circle(screen,(255,255,0),(int(b[0]),int(b[1])),4)

    if boss:
        screen.blit(boss_img, boss.topleft)

    pygame.draw.rect(screen,(80,0,0),(10,10,200,20))
    pygame.draw.rect(screen,(0,255,0),(10,10,200*(hp/max_hp),20))

    screen.blit(font.render(f"Score:{score}",True,(255,255,255)),(10,40))
    screen.blit(font.render(f"Level:{level}",True,(255,255,255)),(10,70))

    if levelup_timer > 0:
        screen.blit(levelup_img,(250,200))
        levelup_timer -= 1

    pygame.display.flip()

pygame.quit()