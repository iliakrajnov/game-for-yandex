import pygame
import cv2
import sys
import os
import random
from PIL import Image
from time import sleep
import tkinter as tk

FPS = 50
all_sprites = pygame.sprite.Group()
root = tk.Tk()


class result_s:
    def __init__(self, g=1):
        self.g = g


    def result_screen(self):
        global score
        intro_text = ["Нажмите на любую клавишу, чтобы начать заново..."]
        screen.fill((0, 0, 0))

        s = score
        score = 0
        title = pygame.font.Font(None, 120).render('ВАШ РУЗУЛЬТАТ: ' + str(s), 1, (255, 0, 0))
        screen.blit(title, ((width - title.get_rect().width) // 2, 200))
        

        font = pygame.font.Font(None, 30)
        text_coord = 400 + title.get_rect().bottom
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = (width - string_rendered.get_rect().width) // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == event.type == pygame.KEYDOWN:
                    sys.exit()       
            pygame.display.flip()
            clock.tick(FPS)

# Стартовый экран в двух фазах
class start_s:
    def __init__(self, g=1):
        self.g = g

    def start_screen(self):
        fon = pygame.transform.scale(pygame.image.load('data/logo.png'), (width, height))
        screen.blit(fon, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def start_screen2(self):
        intro_text = ["Управление интуитивное",
                      "Кнопка Escape для побега",
                      "Нажмите на любую клавишу, чтобы продолжить..."]
        screen.fill((0, 0, 0))

        title = pygame.font.Font(None, 120).render('PONG', 1, (255, 0, 0))
        screen.blit(title, ((width - title.get_rect().width) // 2, 200))

        font = pygame.font.Font(None, 30)
        text_coord = 400 + title.get_rect().bottom
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = (width - string_rendered.get_rect().width) // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        color = [255, 0, 0]
        cycle = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            if cycle == 0:
                color[0] -= 1
                color[1] += 1
                if color == [0, 255, 0]:
                    cycle = 1
            elif cycle == 1:
                color[1] -= 1
                color[2] += 1
                if color == [0, 0, 255]:
                    cycle = 2
            elif cycle == 2:
                color[2] -= 1
                color[0] += 1
                if color == [255, 0, 0]:
                    cycle = 0
            title = pygame.font.Font(None, 120).render('PONG', 1, color)
            screen.blit(title, ((width - title.get_rect().width) // 2, 200))

            pygame.display.flip()
            clock.tick(FPS)


class exit:
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.datas = []

    def button(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("data/exit.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 1050
        sprite.rect.y = 0
        self.buttons.add(sprite)
        self.datas.append([12, 12, 0])

    def move(self):
        global running
        counter = 0
        # Движение шарика и чего угодно
        for sprite in self.buttons:
            x, y = sprite.rect.x, sprite.rect.y
            if self.datas[counter][2] == 0:
                for i in self.mot:
                    if sprite.rect.collidepoint(i):
                        self.datas[counter][2] = 5
                        r = result_s()
                        r.result_screen()
                        running = False
                        break
        self.buttons.draw(screen)

# Шарик
class ball(exit):
    def __init__(self):
        super().__init__()
        self.all_balls = pygame.sprite.Group()
        self.data = []
        self.sound1 = pygame.mixer.Sound('data/boing.wav')

    # Новые шарики
    def new_ball(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("data/ball.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = random.randint(1, 1200)
        sprite.rect.y = random.randint(1, 100)
        self.all_balls.add(sprite)
        self.data.append([12, 12, 0, random.randint(0, 20)])

    def move_ball(self):
        global score
        # Секрет
        counter = 0
        # Движение шарика и чего угодно
        for sprite in self.all_balls:
            x, y = sprite.rect.x, sprite.rect.y
            if self.data[counter][2] == 0:
                for i in self.mot:
                    if sprite.rect.collidepoint(i):
                        if self.data[counter][-1] <= 0:
                            self.all_balls.remove(sprite)
                        self.data[counter][2] = 5
                        horisontal = 0
                        vertical = 0
                        for j in self.mot:
                            if j[0] in range(i[0] - 10, i[0] + 10):
                                horisontal += 1
                            if j[1] in range(i[1] - 10, i[1] + 10):
                                vertical += 1
                        if horisontal > vertical:
                            self.data[counter][0] = -self.data[counter][0]
                            score += 5
                            self.sound1.play()
                            break
                        elif vertical > horisontal:
                            self.data[counter][1] = -self.data[counter][1]
                            score += 5
                            self.sound1.play()
                            break
            else:
                self.data[counter][2] -= 1
            if int(y) <= 0 or int(y) >= height:
                self.data[counter][1] = -self.data[counter][1]
                self.sound1.play()
                self.data[counter][-1] -= 1
            if int(x) <= 0 or int(x) >= width:
                self.data[counter][0] = -self.data[counter][0]
                self.sound1.play()
                self.data[counter][-1] -= 1
            sprite.rect.y += self.data[counter][1]
            sprite.rect.x += self.data[counter][0]
            counter += 1
            # Контроль шариков
            if counter == 11:
                self.all_balls.remove(sprite)
        self.all_balls.draw(screen)


class bomb(ball):
    def __init__(ball, self):
        super().__init__()
        self.all_bombs = pygame.sprite.Group()
        self.data_b = []
        self.sound1 = pygame.mixer.Sound('data/boing.wav')
        self.sound2 = pygame.mixer.Sound('data/boom2.wav')

    def new_bomb(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("data/bomb.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = random.randint(1, 1200)
        sprite.rect.y = random.randint(1, 40)
        self.all_bombs.add(sprite)
        self.data_b.append([12, 12, 0])

    def move_bomb(self):
        global score
        counter = 0
        # Движение бомбы и чего угодно
        for sprite in self.all_bombs:
            x, y = sprite.rect.x, sprite.rect.y
            for i in self.mot:
                if sprite.rect.collidepoint(i):
                    self.sound2.play()
                    score -= 100
                    self.all_bombs.remove(sprite)
                    return 'boom'
            else:
                self.data_b[counter][2] -= 1
            if int(y) <= 0 or int(y) >= height:
                self.data_b[counter][1] = -self.data_b[counter][1]
                self.sound1.play()
            if int(x) <= 0 or int(x) >= width:
                self.data_b[counter][0] = -self.data_b[counter][0]
                self.sound1.play()
            sprite.rect.y += self.data_b[counter][1]
            sprite.rect.x += self.data_b[counter][0]
            counter += 1
            # Контроль бомб
            if counter == 3:
                self.all_bombs.remove(sprite)
        self.all_bombs.draw(screen)


class star(bomb):
    def __init__(bomb, self):
        super().__init__(self)
        self.all_stars = pygame.sprite.Group()
        self.data_s = []
        self.sound1 = pygame.mixer.Sound('data/boing.wav')
        self.sound3 = pygame.mixer.Sound('data/raz.wav')

    def new_star(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("data/star.png")
        sprite.image.set_colorkey((255, 255, 255))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = random.randint(1, width)
        sprite.rect.y = random.randint(1, 100)
        self.all_stars.add(sprite)
        self.data_s.append([12, 12, 0])

    def move_star(self):
        global score
        counter = 0
        # Движение бомбы и чего угодно
        for sprite in self.all_stars:
            x, y = sprite.rect.x, sprite.rect.y
            for i in self.mot:
                if sprite.rect.collidepoint(i):
                    self.sound3.play()
                    score += 100
                    self.all_stars.remove(sprite)
            else:
                self.data_s[counter][2] -= 1
            if int(y) <= 0 or int(y) >= height:
                self.data_s[counter][1] = -self.data_s[counter][1]
                self.sound1.play()
            if int(x) <= 0 or int(x) >= width:
                self.data_s[counter][0] = -self.data_s[counter][0]
                self.sound1.play()
            sprite.rect.y += self.data_s[counter][1]
            sprite.rect.x += self.data_s[counter][0]
            counter += 1
            # Контроль звезд
            if counter == 3:
                self.all_stars.remove(sprite)
        self.all_stars.draw(screen)


class game(star):
    def __init__(self, old):
        super().__init__(self)
        self.old = old
        self.mot = []

    def work(self, img):
        self.img = img.resize(size)
        xs, ys = self.img.size
        pix = self.img.load()
        self.mot = []
        old = self.old
        if old != []:
            for i in range(0, xs, 20):
                for j in range(0, ys, 20):
                    rgb = pix[i, j]
                    rgbol = old[i, j]
                    if rgb[0] not in range(rgbol[0] - 50, rgbol[0] + 50) and rgb[1] not in range(rgbol[1] - 50,
                                                                                                 rgbol[1] + 50) and \
                            pix[i, j][2] not in range(rgbol[2] - 50, rgbol[2] + 50):
                        self.mot.append([i, j])
        self.old = pix

    def draw(self, img):
        self.work(img)
        img = self.img.tobytes()
        img = pygame.image.fromstring(img, size, 'RGB')
        screen.blit(img, (0, 0))
        self.move()
        self.move_ball()
        self.move_star()
        if self.move_bomb() == 'boom':
            for k in range(20):
                x = random.randint(-75, 75)
                y = random.randint(-75, 75)
                for i in self.all_bombs:
                    i.rect.x += x
                    i.rect.y += y
                for i in self.all_balls:
                    i.rect.x += x
                    i.rect.y += y
                for i in self.all_stars:
                    i.rect.x += x
                    i.rect.y += y
                screen.blit(img, (x, y))
                screen.blit(score_label, (250 + x, 10 + y))
                self.all_bombs.draw(screen)
                self.all_balls.draw(screen)
                self.all_stars.draw(screen)
                pygame.display.flip()


# Уря игра
pygame.init()
score = 0
size = width, height = root.winfo_screenwidth(), root.winfo_screenheight()
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
clock = pygame.time.Clock()
s = start_s()
s.start_screen()
s.start_screen2()
running = True

cap = cv2.VideoCapture(0)
g = game([])
g.button()
while running:
    score_label = pygame.font.Font(None, 75).render(str(score), 1, (175, 175, 175))
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    g.new_star()
    g.new_bomb()
    g.new_ball()
    screen.blit(score_label, (250, 10))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    g.draw(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))