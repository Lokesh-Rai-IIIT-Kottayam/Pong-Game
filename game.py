import pygame
from network import Network
from random import randint

width = 500
height = 500
w = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")



class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 2

    def draw(self, w):
        pygame.draw.rect(w, self.color, self.rect)
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:

            if self.x>0: self.x -= self.vel
            else: self.x = self.x

        if keys[pygame.K_RIGHT]:
            if self.x<400: self.x += self.vel
            else: self.x = self.x

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.cir = ((0,0,255),(cx,cy),5)
        self.m = self.n = 1
    def draw(self, w):
        pygame.draw.circle(w, *self.cir)
    def update(self):
        self.cir = ((0,0,255),(self.cx,self.cy),5)

def read_pos(s):
    s = s.split(",")
    return int(s[0]), int(s[1]), int(s[2]), int(s[3])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])


def redrawwdow(w,player, player2,b):
    w.fill((255,255,255))
    player.draw(w)
    player2.draw(w)
    b.draw(w)
    pygame.display.update()


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0],startPos[1],100,2,(0,255,0))
    p2 = Player(100,50,100,2,(255,0,0))
    b = Ball(startPos[2], startPos[3])
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y, b.cx, b.cy))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        b.cx = p2Pos[2]
        b.cy = p2Pos[3]
        p2.update()
        b.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawwdow(w, p, p2,b)

main()