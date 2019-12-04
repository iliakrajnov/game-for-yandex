import pygame
import cv2
from PIL import Image

class ball:
    def __init__(self):
        self.all_balls = pygame.sprite.Group()
        self.data = []
        self.sound1 = pygame.mixer.Sound('boing.wav')

    def new_ball(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("ball.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 500
        sprite.rect.y = 10
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
            if int(y) <= 0 or int(y) >= 960:
                self.data[counter][1] = -self.data[counter][1]
                self.sound1.play()
            if int(x) <= 0 or int(x) >= 1280:
                self.data[counter][0] = -self.data[counter][0]
                self.sound1.play()
            sprite.rect.y += self.data[counter][1]
            sprite.rect.x += self.data[counter][0]
            counter += 1
        self.all_balls.draw(screen)



class game(ball):
    def __init__(self, old):
        super().__init__()
        self.old = old
        self.mot = []

        
    def work(self, img):
        self.img = img.resize((1280, 960))
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
        img = pygame.image.fromstring(img, (1280, 960), 'RGB')
        screen.blit(img, (0,0))
        self.move()


pygame.init()
size = width, height = 1280, 960
screen = pygame.display.set_mode(size)
running = True
cap = cv2.VideoCapture(0)
g = game([])
g.new_ball()
while running:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    g.draw(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)))
