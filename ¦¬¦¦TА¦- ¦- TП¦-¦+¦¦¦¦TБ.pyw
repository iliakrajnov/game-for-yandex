import pygame
import cv2
from PIL import Image

class game:
    def __init__(self, old):
        self.old = old
        self.mot = []
        self.x = 500
        self.y = 10
        self.vy = 7
        self.vx = 7
        self.stop = 0
        self.sound1 = pygame.mixer.Sound('boing.wav')

        
    def work(self, img):
        self.img = img.resize((1280, 960))
        xs, ys = self.img.size
        pix = self.img.load()
        self.mot = []
        old = self.old
        if old != []:
            for i in range(0, xs, 10):
                for j in range(0, ys, 10):
                    if pix[i, j][0] not in range(old[i, j][0] - 20, old[i, j][0] + 20) and pix[i, j][1] not in range(old[i, j][1] - 50, old[i, j][1] + 50) and pix[i, j][2] not in range(old[i, j][2] - 50, old[i, j][2] + 50):
                        self.mot.append([i, j])
                        
        self.old = pix

    def ball(self):
        screen.blit(pygame.image.load('ball.png'), (self.x - 40, self.y - 40))
        #pygame.draw.circle(screen, pygame.Color('green'), (self.x, int(self.y)), 20)
        if self.stop == 0:
            for i in self.mot:
                if int(self.y) in range(i[1] - 20, i[1] + 20) and int(self.x) in range(i[0] - 20, i[0] + 20):
                    self.stop = 5
                    for j in self.mot:
                        if j[0] in range(i[0] - 20, i[0] + 20):
                            self.vx = -self.vx
                            self.sound1.play()
                            break
                        elif j[1] in range(i[1] - 20, i[1] + 20):
                            self.vy = -self.vy
                            self.sound1.play()
                            break
                    break
        else:
            self.stop -= 1
        if int(self.y) <= 0 or int(self.y) >= 960:
            self.vy = -self.vy
            self.sound1.play()
        if int(self.x) <= 0 or int(self.x) >= 1280:
            self.vx = -self.vx
            self.sound1.play()
        self.y += self.vy
        self.x += self.vx
        

        
    def draw(self, screen, img):
        self.work(img)
        img = self.img.tobytes()
        img = pygame.image.fromstring(img, (1280, 960), 'RGB')
        screen.blit(img, (0,0))
        self.ball()


pygame.init()
size = width, height = 1280, 960
screen = pygame.display.set_mode(size)
running = True
cap = cv2.VideoCapture(0)
old = []
g = game(old)
while running:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    g.draw(screen, Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)))
