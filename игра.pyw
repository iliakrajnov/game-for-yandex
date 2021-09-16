import random
import sys
import tkinter as tk
from time import time

import os
import cv2
import pygame

FPS = 60
all_sprites = pygame.sprite.Group()
root = tk.Tk()
score = 0
size = width, height = root.winfo_screenwidth(), root.winfo_screenheight()

screen = pygame.display.set_mode(
    size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
clock = pygame.time.Clock()


def send(text):
    with open("data/records.csv", 'w', encoding="utf8") as ast:
        ast.write(text)


def get_table():
    with open("data/records.csv", encoding="utf8") as ast:
        return ast.read()



def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    image = pygame.image.load(fullname)
    return image


class leader_table_s:
    def __init__(self, data):
        self.data = data

    def leaders(self):
        global score
        screen.fill((0, 0, 0))

        title = pygame.font.Font(None, 120).render("Таблица лидеров", 1, (0, 255, 0))
        screen.blit(title, (100, 100))

        font = pygame.font.Font(None, 30)
        text_coord = 120 + title.get_rect().bottom
        text_x = 100
        pygame.display.flip()
        for line in self.data:
            string_rendered = font.render(" :".join(line), 1, pygame.Color("white"))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = text_x
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            if text_coord >= height:
                text_coord = 120 + title.get_rect().bottom
                text_x += 250
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    gameover_screen()

            title = pygame.font.Font(None, 120).render(
                "Таблица лидеров", 1, (0, 255, 0)
            )
            screen.blit(title, (100, 100))
            pygame.display.flip()
            clock.tick(FPS)


class error:
    def __init__(self, g=1):
        self.g = g

    def gameover_screen(self):
        global score
        screen.fill((0, 0, 0))
        intro_text = [
            'Нажмите на кнопку "Escape", чтобы выйти на улицу',
            "Enter - чтобы купить веб-камеру",
        ]
        title = pygame.font.Font(None, 120).render(
            "Нужна вебка", 1, pygame.Color("white")
        )
        screen.blit(title, ((width - title.get_rect().width) // 2, 200))
        font = pygame.font.Font(None, 30)
        text_coord = 200 + title.get_rect().bottom
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color("white"))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = (width - string_rendered.get_rect().width) // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                    elif event.key == pygame.K_RETURN:
                        os.system("start https://www.e-katalog.ru/list/201/pr-7488/")

            pygame.display.flip()
            clock.tick()


class start_s:
    def __init__(self, g=1):
        self.g = g

    def start_screen(self):
        fon = pygame.transform.scale(load_image("logo.png"), (width, height))
        screen.blit(fon, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                if (
                        event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN
                ):
                    return
            title = pygame.font.Font(None, 24).render(
                "Внимание, ИГРА МОЖЕТ ВЫЗЫВАТЬ ПРИПАДКИ ЭПИЛЕПСИИ! нажмите на любую клавишу для продолжения, esc - для выхода.",
                1, (255, 0, 0))
            screen.blit(title, ((width - title.get_rect().width) // 2, height - 20))
            pygame.display.flip()
            clock.tick(FPS)

    def start_screen2(self):
        intro_text = [
            "Управление интуитивное - двигайтесь и собирайте звездочки, уворачиваясь от бомб",
            "Кнопка Escape для выхода",
            "Нажмите на любую клавишу, чтобы продолжить...",
            "",
            "Разработчики - Илья Крайнов и Алексей Попович",
            "Мудрый учитель - Екатерина Филина"
        ]
        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 30)
        text_coord = 500
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color("white"))
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
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
            title = pygame.font.Font(None, 120).render("PONG", 1, color)
            subtitle = pygame.font.Font(None, 60).render("Triumf edition", 1, color)
            screen.blit(title, ((width - title.get_rect().width) // 2, 200))
            screen.blit(subtitle, ((width - subtitle.get_rect().width) // 2, 300))

            pygame.display.flip()
            clock.tick(FPS)
    
    def loading_screen(self):
        screen.fill((0, 0, 0))
        title = pygame.font.Font(None, 120).render("ЗАГРУЗКА,", 1, pygame.Color("white"))
        subtitle = pygame.font.Font(None, 60).render("которая не займет больше 20 секунд. Обещаем!", 1, pygame.Color("white"))
        screen.blit(title, ((width - title.get_rect().width) // 2, 200))
        screen.blit(subtitle, ((width - subtitle.get_rect().width) // 2, 300))

        intro_text = [
            "Сейчас мы настраиваем оборудование наилучшим образом, как только можем представить",
            "",
            "Разработчики - Илья Крайнов и Алексей Попович",
            "Мудрый учитель - Екатерина Филина"
        ]

        font = pygame.font.Font(None, 30)
        text_coord = 500
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color("white"))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = (width - string_rendered.get_rect().width) // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        return 


def gameover_screen():
    global score
    global records
    records = list(reversed(sorted(records, key=lambda i: int(i[1]))))
    screen.fill((0, 0, 0))
    intro_text = [
        'Нажмите на кнопку "Escape", чтобы выйти из игры, Зажмите "Shift" - для просмотра таблицы лидеров.',
        "Enter - начать заново",
        "",
        f"Лучший | {': '.join(records[0])}",
        f"Ты     | {score}",
        "Ваше имя:",
    ]
    title = pygame.font.Font(None, 120).render("Game Over.", 1, pygame.Color("white"))
    screen.blit(title, ((width - title.get_rect().width) // 2, 200))
    font = pygame.font.Font(None, 30)
    text_coord = 200 + title.get_rect().bottom
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color("white"))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (width - string_rendered.get_rect().width) // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if name != "":
                        records.append([name, str(score)])
                        ok = ''
                        for i in records:
                            ok += ';'.join(i) + '\n'
                        send(ok)
                    pygame.quit()
                    raise SystemExit
                elif event.key == pygame.K_RETURN:
                    if name != "":
                        records.append([name, str(score)])
                        ok = ''
                        for i in records:
                            ok += ';'.join(i) + '\n'
                        send(ok)
                    score = 0
                    g.restart()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    table = leader_table_s(records)
                    table.leaders()
                else:
                    name += chr(int(event.key))
                    if len(name) > 20:
                        name = name[:20]
                title = pygame.font.Font(None, 120).render(
                    name, 1, pygame.Color("white")
                )
                pygame.draw.rect(screen, (0, 0, 0), (0, 500, 10000, 500))
                screen.blit(title, ((width - title.get_rect().width) // 2, 500))

        pygame.display.flip()
        clock.tick()


class exit:
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.datas = []

    def button(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("data/exit.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = width - 300
        sprite.rect.y = 0
        self.buttons.add(sprite)

    def move(self):
        global score
        # Секрет
        counter = 0
        # Движение шарика и чего угодно
        for sprite in self.buttons:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if sprite.rect.collidepoint((x, y)):
                        gameover_screen()
        self.buttons.draw(screen)


# Шарик
class ball(exit):
    def __init__(self):
        super().__init__()
        self.all_balls = pygame.sprite.Group()
        self.data = []
        self.sound1 = pygame.mixer.Sound("data/boing.wav")

    # Новые шарики
    def new_ball(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("data/ball.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = random.randint(1, 1200)
        sprite.rect.y = random.randint(1, 100)
        self.all_balls.add(sprite)
        self.data.append([12, 12, 0])

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
            if int(x) <= 0 or int(x) >= width:
                self.data[counter][0] = -self.data[counter][0]
                self.sound1.play()
            sprite.rect.y += self.data[counter][1]
            sprite.rect.x += self.data[counter][0]
            counter += 1
            # Контроль шариков
        if counter < 10:
            self.new_ball()
        self.all_balls.draw(screen)


class bomb(ball):
    def __init__(ball, self):
        super().__init__()
        self.all_bombs = pygame.sprite.Group()
        self.data_b = []
        self.sound1 = pygame.mixer.Sound("data/boing.wav")
        self.sound2 = pygame.mixer.Sound("data/boom2.wav")

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
                if sprite.rect.collidepoint(i) and self.data_b[counter][2] == 0:
                    self.sound2.play()
                    score -= 100
                    self.data_b[counter][2] = 1
                    sprite.image = pygame.image.load("data/boom.png")
            if int(y) <= 0 or int(y) >= height:
                self.data_b[counter][1] = -self.data_b[counter][1]
                self.sound1.play()
            if int(x) <= 0 or int(x) >= width:
                self.data_b[counter][0] = -self.data_b[counter][0]
                self.sound1.play()
            
            if self.data_b[counter][2] == 0:
                sprite.rect.y += self.data_b[counter][1]
                sprite.rect.x += self.data_b[counter][0]
            elif self.data_b[counter][2] >= 10:
                self.all_bombs.remove(sprite)
                del self.data_b[counter]
                counter -= 1
            elif self.data_b[counter][2] > 0:
                self.data_b[counter][2] += 1
            counter += 1
            # Контроль бомб
        if counter < 3:
            self.new_bomb()
        self.all_bombs.draw(screen)


class star(bomb):
    def __init__(bomb, self):
        super().__init__(self)
        self.all_stars = pygame.sprite.Group()
        self.data_s = []
        self.sound1 = pygame.mixer.Sound("data/boing.wav")
        self.sound3 = pygame.mixer.Sound("data/raz.wav")

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
                    del self.data_s[counter]
                    break
            else:
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
        if counter < 3:
            self.new_star()
        self.all_stars.draw(screen)


class game(star):
    def __init__(self, old):
        super().__init__(self)
        self.old = old
        self.mot = []
    
    def restart(self):
        s = start_s()
        s.start_screen()
        s.start_screen2()
        s.loading_screen()
        start()

    def work(self, img):
        img = cv2.resize(img, size, cv2.INTER_NEAREST)
        if self.old != []:
            self.mot = []
            diff = cv2.absdiff(self.old, img)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # перевод кадров в черно-белую градацию
            blur = cv2.GaussianBlur(gray, (5, 5), 0) # фильтрация лишних контуров 
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) # метод для выделения кромки объекта белым цветом
            dilated = cv2.dilate(thresh, None, iterations = 3) # данный метод противоположен методу erosion(), т.е. эрозии объекта, и расширяет выделенную на предыдущем этапе область
            mot, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for i in mot:
                if  cv2.contourArea(i) >= 700:
                    for j in i.tolist():
                        self.mot.append(j[0])
            
            self.old = img
            self.img = img
        else:
            self.img = img
            self.old = img

    def draw(self, img):
        global score_label
        global start_time
        if time() - start_time >= 1800:
            gameover_screen()
        self.work(img)
        img = pygame.image.frombuffer(self.img.tostring(), self.img.shape[1::-1], "RGB")
        screen.blit(img, (0, 0))
        '''moved_x = 0
        moved_y = 0
        if self.move_bomb() == "boom":
            for k in range(2):
                x = random.randint(-75, 75)
                y = random.randint(-75, 75)
                moved_x += x
                moved_y += y
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
                screen.blit(time_label, (750 + x, 10 + y))
                self.all_bombs.draw(screen)
                self.all_balls.draw(screen)
                self.all_stars.draw(screen)
                pygame.display.flip()
            for i in self.all_bombs:
                i.rect.x -= moved_x
                i.rect.y -= moved_y
            for i in self.all_balls:
                i.rect.x -= moved_x
                i.rect.y -= moved_y
            for i in self.all_stars:
                i.rect.x -= moved_x
                i.rect.y -= moved_y'''
        screen.blit(score_label, (250, 10))
        screen.blit(time_label, (750, 10))
        self.move()
        self.move_ball()
        self.move_star()
        self.move_bomb()
        self.all_bombs.draw(screen)
        self.all_balls.draw(screen)
        self.all_stars.draw(screen)
        pygame.display.flip()


def start():
    global score_label
    global time_label
    global records
    global start_time
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    work, _ = cap.read()
    if not work:
        error().gameover_screen()
    start_time = time()
    records = []
    for i in get_table().splitlines():
        records.append(i.split(';'))
    running = True
    g = game([])
    g.button()
    while running:
        pygame.time.Clock().tick(80)
        score_label = pygame.font.Font(None, 75).render(str(score), 1, (175, 175, 175))
        time_label = pygame.font.Font(None, 75).render(
            str(int(1800 - (time() - start_time))) + " Сек.", 1, (175, 175, 175)
        )
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        screen.blit(score_label, (250, 10))
        screen.blit(time_label, (750, 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameover_screen()
        g.draw(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


# Уря игра
pygame.init()
g = game([])
g.restart()
