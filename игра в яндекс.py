import pygame
import cv2
import sys
import os
import random
from PIL import Image


FPS = 50
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image

def start_screen():
    fon = pygame.transform.scale(load_image('logo.png'), (1280, 600))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

def start_screen2():
    intro_text = ["Управление интуетивное",
                  "Нажмите на любую клавишу, чтобы продолжить..."]
    screen.fill((0, 0, 0))

    title = pygame.font.Font(None, 120).render('PONG', 1, (255, 0, 0))
    screen.blit(title, ((width - title.get_rect().width) // 2, 200))

    font = pygame.font.Font(None, 30)
    text_coord = 200 + title.get_rect().bottom
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

class ball:
    def __init__(self):
        self.all_balls = pygame.sprite.Group()
        self.data = []
        self.sound1 = pygame.mixer.Sound('boing.wav')

    def new_ball(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("ball.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = random.randint(1,1200)
        sprite.rect.y = random.randint(1, 40)
        self.all_balls.add(sprite)
        self.data.append([12, 12, 0])
        
    def move(self):
        counter = 0
        for sprite in self.all_balls:
            x, y = sprite.rect.x, sprite.rect.y
            if self.data[counter][2] == 0:
                for i in self.mot:
                    if sprite.rect.collidepoint(i):
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
                            self.sound1.play()
                            break
                        elif vertical > horisontal:
                            self.data[counter][1] = -self.data[counter][1]
                            self.sound1.play()
                            break
            else:
                self.data[counter][2] -= 1
            if int(y) <= 0 or int(y) >= 600:
                self.data[counter][1] = -self.data[counter][1]
                self.sound1.play()
            if int(x) <= 0 or int(x) >= 1280:
                self.data[counter][0] = -self.data[counter][0]
                self.sound1.play()
            sprite.rect.y += self.data[counter][1]
            sprite.rect.x += self.data[counter][0]
            counter += 1
        self.all_balls.draw(screen)


class bomb(ball):
    def new_bomb(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("bomb.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = random.randint(1,1200)
        sprite.rect.y = random.randint(1, 40)
        self.all_balls.add(sprite)
        self.data.append([12, 12, 0])

    # def move(self):
    #     counter = 0
    #     for sprite in self.all_balls:
    #         x, y = sprite.rect.x, sprite.rect.y
    #         if self.data[counter][2] == 0:
    #             for i in self.mot:
    #                 if sprite.rect.collidepoint(i):
    #                     self.data[counter][2] = 5
    #                     horisontal = 0
    #                     vertical = 0
    #                     for j in self.mot:
    #                         if j[0] in range(i[0] - 10, i[0] + 10):
    #                             horisontal += 1
    #                         if j[1] in range(i[1] - 10, i[1] + 10):
    #                             vertical += 1
    #                     if horisontal > vertical:
    #                         self.data[counter][0] = -self.data[counter][0]
    #                         self.sound1.play()
    #                         break
    #                     elif vertical > horisontal:
    #                         self.data[counter][1] = -self.data[counter][1]
    #                         self.sound1.play()
    #                         break
    #         else:
    #             self.data[counter][2] -= 1
    #         if int(y) <= 0 or int(y) >= 600:
    #             self.data[counter][1] = -self.data[counter][1]
    #             self.sound1.play()
    #         if int(x) <= 0 or int(x) >= 1280:
    #             self.data[counter][0] = -self.data[counter][0]
    #             self.sound1.play()
    #         sprite.rect.y += self.data[counter][1]
    #         sprite.rect.x += self.data[counter][0]
    #         counter += 1
    #     self.all_balls.draw(screen)

class game(bomb):
    def __init__(self, old):
        super().__init__()
        self.old = old
        self.mot = []



        
    def work(self, img):
        self.img = img.resize((1280, 600))
        xs, ys = self.img.size
        pix = self.img.load()
        self.mot = []
        old = self.old
        if old != []:
            for i in range(0, xs, 20):
                for j in range(0, ys, 20):
                    rgb = pix[i, j]
                    rgbol = old[i, j]
                    if rgb[0] not in range(rgbol[0] - 50, rgbol[0] + 50) and rgb[1] not in range(rgbol[1] - 50, rgbol[1] + 50) and pix[i, j][2] not in range(rgbol[2] - 50, rgbol[2] + 50):
                        self.mot.append([i, j])
                        
        self.old = pix

        
    def draw(self, img):
        self.work(img)
        img = self.img.tobytes()
        img = pygame.image.fromstring(img, (1280, 600), 'RGB')
        screen.blit(img, (0,0))
        self.move()


pygame.init()
size = width, height = 1280, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_screen()
start_screen2()
running = True

cap = cv2.VideoCapture(0)
g = game([])
g.new_ball()
g.new_bomb()
while running:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    g.draw(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
