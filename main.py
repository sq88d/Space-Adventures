import os
import sys
import pygame
import random
from os import path
from pygame.locals import FULLSCREEN

# создание окна программы
pygame.init()
pygame.mixer.init()  # звуки
pygame.font.init()  # шрифты
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
pygame.display.set_caption("Space Adventures")

# получение разрешения экрана
info_screen = pygame.display.Info()
WIDTH, HEIGHT = info_screen.current_w, info_screen.current_h

# константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MEDIUM_PURPLE = (147, 112, 219)
BLUE_VIOLET = (138, 43, 226)
SLATE_BLUE = (106, 90, 205)
DARK_SLATE_BLUE = (72, 61, 139)
INDIGO = (75, 0, 130)
PURPLE = (128, 0, 128)

FPS = 60
SCORE = 0
GAME_COEF = WIDTH / 1920
image_count = 1

game_go = True
music_on = True
sounds_on = True
start_game = False
game_mode = ''

# скорость
clock = pygame.time.Clock()

# подключение музыкальных файлов
laser_sound = pygame.mixer.Sound('music/laser1.ogg')
button_sound = pygame.mixer.Sound('music/button2.flac')


# загрузка изображений
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image


# настройки
def settings():
    global music_on, sounds_on

    running_settings = True
    while running_settings:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running_settings = False

            screen.fill(BLACK)
            print_text('Settings', 700, 50, WHITE, 'fonts/Teletactile.ttf', 80)
            print_text('Music', 760, 300, WHITE)
            print_text('Sounds', 760, 350, WHITE)

            button_start_screen1 = Button(100 * GAME_COEF, 40 * GAME_COEF, BLACK, BLACK)
            button_start_screen2 = Button(100 * GAME_COEF, 40 * GAME_COEF, BLACK, BLACK)
            button_start_screen3 = Button(100 * GAME_COEF, 40 * GAME_COEF, BLACK, BLACK)

            button_start_screen3.draw(900 * GAME_COEF, HEIGHT - 100, 'back')

            if music_on is True:
                button_start_screen1.draw(1100 * GAME_COEF, 290, 'on')
            else:
                button_start_screen1.draw(1100 * GAME_COEF, 290, 'off')

            if sounds_on is True:
                button_start_screen2.draw(1100 * GAME_COEF, 340, 'on')
            else:
                button_start_screen2.draw(1100 * GAME_COEF, 340, 'off')

            # music
            if 1100 * GAME_COEF * GAME_COEF < mouse[0] < 1100 * GAME_COEF + 100 * GAME_COEF and 290 < mouse[
                1] < 290 + 40 * GAME_COEF and click[0] == 1:
                if sounds_on:
                    pygame.mixer.Sound.play(button_sound)

                if music_on is True:
                    music_on = False
                else:
                    music_on = True

            # sounds
            if 1100 * GAME_COEF * GAME_COEF < mouse[0] < 1100 * GAME_COEF + 100 * GAME_COEF and 340 < mouse[
                1] < 340 + 40 * GAME_COEF and click[0] == 1:
                if sounds_on:
                    pygame.mixer.Sound.play(button_sound)

                if sounds_on is True:
                    sounds_on = False
                else:
                    sounds_on = True

            # back
            if 900 * GAME_COEF * GAME_COEF < mouse[0] < 900 * GAME_COEF + 100 * GAME_COEF and HEIGHT - 100 < mouse[
                1] < HEIGHT - 100 + 40 * GAME_COEF and click[0] == 1:
                if sounds_on:
                    pygame.mixer.Sound.play(button_sound)

                running_settings = False

            pygame.display.update()
            clock.tick(60)


# стартовый экран
def start_screen():
    global image_count, game_go, sounds_on

    start = True
    while start:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                start = False
                game_go = False

            screen.fill(BLACK)
            print_text('Space Adventures', 830, 50, WHITE, 'fonts/Teletactile.ttf', 80)

            # вращающийся земной шар
            if image_count == 238:
                image_count = 1

            if 1 <= image_count <= 119:
                start_image = load_image(f'Earth/{image_count}.png')
                start_image = pygame.transform.scale(start_image, (810 * GAME_COEF, 810 * GAME_COEF))
                rect = start_image.get_rect()
                rect.x = 100
                rect.y = 100
                image_count += 1
                screen.blit(start_image, rect)

            elif image_count == 120:
                start_image = load_image(f'Earth/{121}.png')
                start_image = pygame.transform.scale(start_image, (810 * GAME_COEF, 810 * GAME_COEF))
                rect = start_image.get_rect()
                rect.x = 100
                rect.y = 100
                image_count += 1
                screen.blit(start_image, rect)

            elif 120 < image_count <= 239:
                start_image = load_image(f'Earth/{image_count}.png')
                start_image = pygame.transform.scale(start_image, (810 * GAME_COEF, 810 * GAME_COEF))
                rect = start_image.get_rect()
                rect.x = 100
                rect.y = 100

                image_count += 1
                screen.blit(start_image, rect)

            # кнопки
            button_start_screen1 = Button(320 * GAME_COEF, 50 * GAME_COEF, SLATE_BLUE, DARK_SLATE_BLUE)
            button_start_screen2 = Button(320 * GAME_COEF, 50 * GAME_COEF, SLATE_BLUE, DARK_SLATE_BLUE)
            button_start_screen3 = Button(320 * GAME_COEF, 50 * GAME_COEF, SLATE_BLUE, DARK_SLATE_BLUE)

            button_start_screen1.draw(WIDTH - 400 * GAME_COEF, HEIGHT - 200, 'Play')
            button_start_screen2.draw(WIDTH - 400 * GAME_COEF, HEIGHT - 150, 'Settings')
            button_start_screen3.draw(WIDTH - 400 * GAME_COEF, HEIGHT - 100, 'Quit game')

            # активация start_game
            if WIDTH - 400 * GAME_COEF < mouse[0] < WIDTH - 400 * GAME_COEF + 350 * GAME_COEF and HEIGHT - 200 < mouse[
                1] < HEIGHT - 200 + 50 * GAME_COEF and click[0] == 1:
                if sounds_on:
                    pygame.mixer.Sound.play(button_sound)

                start = False

            # активация settings
            elif WIDTH - 400 * GAME_COEF < mouse[0] < WIDTH - 400 * GAME_COEF + 350 * GAME_COEF and HEIGHT - 200 < \
                    mouse[
                        1] < HEIGHT - 150 + 50 * GAME_COEF and click[0] == 1:
                if sounds_on:
                    pygame.mixer.Sound.play(button_sound)

                settings()

            # активация quit_game
            elif WIDTH - 400 * GAME_COEF < mouse[0] < WIDTH - 400 * GAME_COEF + 350 * GAME_COEF and HEIGHT - 200 < \
                    mouse[
                        1] < HEIGHT - 100 + 50 * GAME_COEF and click[0] == 1:
                if sounds_on:
                    pygame.mixer.Sound.play(button_sound)

                game_go = False
                start = False

            pygame.display.update()
            clock.tick(120)


# пауза игры
def pause():
    paused = True
    while paused:

        for event in pygame.event.get():

            # Проверка на закрытие окна
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            print_text('Paused. Press P or Enter to continue', WIDTH // 5, HEIGHT // 2, WHITE)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] or keys[pygame.K_p]:
                paused = False

            pygame.display.update()
            clock.tick(15)


# окончание игры
def game_over():
    stopped = True
    while stopped:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            print_text('Game Over', 820, 520, WHITE)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                stopped = False

            pygame.display.update()
            clock.tick(15)


# вывод текста на экран
def print_text(message, x, y, font_color=WHITE, font_type='fonts/Teletactile.ttf', font_size=int(40 * GAME_COEF)):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


# создание кнопок
class Button:
    def __init__(self, width, height, inactive_color, active_color):  # высота, ширина кнопки
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color

    def draw(self, x, y, message):  # расположение, текст
        mouse = pygame.mouse.get_pos()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

        print_text(message, x + 10, y + 10)


# игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_image = load_image('SpaceShip1.png')
        player_image = pygame.transform.scale(player_image, (100 * GAME_COEF, 100 * GAME_COEF))

        self.image = player_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(player_image)

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10 * GAME_COEF
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -8 * GAME_COEF
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8 * GAME_COEF

        self.rect.x += self.speedx

        if self.rect.right > (WIDTH // 4 * 3):
            self.rect.right = WIDTH // 4 * 3

        if self.rect.left < (WIDTH // 4):
            self.rect.left = WIDTH // 4

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# звезды
class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


# астероиды
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        asteroid_image = load_image('asteroid_brow.png')
        asteroid_image = pygame.transform.scale(asteroid_image, (50 * GAME_COEF, 50 * GAME_COEF))

        self.image = asteroid_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(asteroid_image)

        self.rect.x = random.randrange(WIDTH // 4, WIDTH // 4 * 3)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        if not pygame.sprite.collide_mask(self, player):
            self.rect.x += self.speedx * GAME_COEF
            self.rect.y += self.speedy * GAME_COEF
            if self.rect.top > HEIGHT + 10 or self.rect.left < WIDTH // 4 or self.rect.right > WIDTH // 4 * 3:
                self.rect.x = random.randrange(WIDTH // 4, WIDTH // 4 * 3)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)


# враги
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


# пули игрока
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bullet_image = load_image('bullet2_dark.png')
        bullet_image = pygame.transform.scale(bullet_image, (21 * GAME_COEF, 40 * GAME_COEF))

        self.image = bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        # Удаление пули, если она за экраном
        if self.rect.bottom < 0:
            self.kill()


# загрузка картинок
background_image = load_image('background2.jpg')
background_image = pygame.transform.scale(background_image, (1920 * GAME_COEF, 1080 * GAME_COEF))
background_rect = background_image.get_rect()

# создание групп спрайтов
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# запуск классов
player = Player()
all_sprites.add(player)

for i in range(11):
    a = Asteroid()
    all_sprites.add(a)
    asteroids.add(a)


def run_game():
    global SCORE, start_game, game_mode

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_game:
                    pygame.mixer.Sound.play(laser_sound)
                    player.shoot()

                if event.key == pygame.K_p:
                    pause()

        # обновление
        screen.blit(background_image, background_rect)

        # создание кнопок меню на главном экране
        button_start_game = Button(350 * GAME_COEF, 50 * GAME_COEF, PURPLE, INDIGO)
        button_settings = Button(350 * GAME_COEF, 50 * GAME_COEF, PURPLE, INDIGO)
        button_game_quit = Button(350 * GAME_COEF, 50 * GAME_COEF, PURPLE, INDIGO)

        # отрисовка кнопок меню на главном экране
        button_start_game.draw(30 * GAME_COEF, HEIGHT - 200 * GAME_COEF, 'Start game')
        button_settings.draw(30 * GAME_COEF, HEIGHT - 150 * GAME_COEF, 'Settings')
        button_game_quit.draw(30 * GAME_COEF, HEIGHT - 100 * GAME_COEF, 'Quit')

        # start game
        if 30 * GAME_COEF * GAME_COEF < mouse[0] < 30 * GAME_COEF + 350 * GAME_COEF and HEIGHT - 200 < mouse[
            1] < HEIGHT - 200 + 50 * GAME_COEF and click[0] == 1:
            if sounds_on:
                pygame.mixer.Sound.play(button_sound)
            start_game = True

        # settings
        if 30 * GAME_COEF * GAME_COEF < mouse[0] < 30 * GAME_COEF + 350 * GAME_COEF and HEIGHT - 150 < mouse[
            1] < HEIGHT - 150 + 50 * GAME_COEF and click[0] == 1:
            if sounds_on:
                pygame.mixer.Sound.play(button_sound)
            settings()

        # quit game
        if 30 * GAME_COEF * GAME_COEF < mouse[0] < 30 * GAME_COEF + 350 * GAME_COEF and HEIGHT - 100 < mouse[
            1] < HEIGHT - 100 + 50 * GAME_COEF and click[0] == 1:
            if sounds_on:
                pygame.mixer.Sound.play(button_sound)
            running = False

        # отрисовка текста на главном экране
        print_text('Space Adventures', 20 * GAME_COEF, 30 * GAME_COEF, WHITE, 'fonts/Teletactile.ttf', 60)
        print_text(f'Scores: {SCORE}', (WIDTH - 400) * GAME_COEF, 50 * GAME_COEF)

        if start_game:
            # создание кнопок выбора режима игры
            button_infinite_mode = Button(450 * GAME_COEF, 50 * GAME_COEF, PURPLE, INDIGO)
            button_levels = Button(450 * GAME_COEF, 50 * GAME_COEF, PURPLE, INDIGO)

            # отрисовка кнопок
            button_infinite_mode.draw(30 * GAME_COEF, 150 * GAME_COEF, 'Infinite mode')
            button_levels.draw(30 * GAME_COEF, 200 * GAME_COEF, 'Levels')

            # infinite
            if 30 * GAME_COEF * GAME_COEF < mouse[0] < 30 * GAME_COEF + 450 * GAME_COEF and 150 * GAME_COEF < mouse[
                1] < 150 * GAME_COEF + 50 * GAME_COEF and click[0] == 1:
                if sounds_on:
                    pygame.mixer.Sound.play(button_sound)
                game_mode = 'Infinite'

            # levels
            if 30 * GAME_COEF * GAME_COEF < mouse[0] < 30 * GAME_COEF + 450 * GAME_COEF and 200 * GAME_COEF < mouse[
                1] < 200 * GAME_COEF + 50 * GAME_COEF and click[0] == 1:
                if sounds_on:
                    pygame.mixer.Sound.play(button_sound)
                game_mode = 'Levels'

            if game_mode == 'Infinite':
                all_sprites.update()
                # проверка на попадание врага в игрока
                hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
                for hit in hits:
                    m = Mob()
                    all_sprites.add(m)
                    mobs.add(m)

                # проверка на попадание пули в астероид
                hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
                for hit in hits:
                    SCORE += 3
                    a = Asteroid()
                    all_sprites.add(a)
                    asteroids.add(a)
                    all_sprites.update()
                    all_sprites.draw(screen)

                # проверка на попадание астероида в игрока
                hits = pygame.sprite.spritecollide(player, asteroids, False)
                if hits:
                    game_over()

                all_sprites.draw(screen)

            elif game_mode == 'Levels':
                # создание кнопок выбора режима игры
                button_level1 = Button(450 * GAME_COEF, 50 * GAME_COEF, PURPLE, INDIGO)
                button_level2 = Button(450 * GAME_COEF, 50 * GAME_COEF, PURPLE, INDIGO)
                button_level3 = Button(450 * GAME_COEF, 50 * GAME_COEF, PURPLE, INDIGO)

                # отрисовка кнопок
                button_level1.draw(30 * GAME_COEF, 300 * GAME_COEF, '1')
                button_level2.draw(30 * GAME_COEF, 350 * GAME_COEF, '2')
                button_level3.draw(30 * GAME_COEF, 400 * GAME_COEF, '3')

        pygame.display.flip()
        clock.tick(FPS)


start_screen()
if game_go is True:
    run_game()
