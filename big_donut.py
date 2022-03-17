import pygame
import math
from pygame.locals import *
from sys import exit

pygame.init()

WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
font = pygame.font.SysFont('Arial', 10, bold=True)

x_offset = WIDTH / 2
y_offset = HEIGHT / 2

r1 = 80 #radius 2D circle
r2 = 150 #distance from center / radius torus
A, B = 1, 1 #rotation angles x- and z-axis
K2 = 5000
K1 = WIDTH * K2 * 3/(8*(r1 + r2))

x_space = 10
y_space = 12
col = int(WIDTH // x_space)
rows = int(HEIGHT // y_space)


chars = ['.', ',', '-', '~', ':', ';', '=', '!', '*', '#', '$', '@']


def draw(x, y, char):
    text = font.render(char, True, WHITE)
    screen.blit(text, (x, y))

while True:
    screen.fill((BLACK)) #erase previous donut
    cosB, sinB = math.cos(B), math.sin(B)
    cosA, sinA = math.cos(A), math.sin(A)

    output = []
    for i in range(rows):
        col1 = []
        for j in range(col):
            col1.append(" ")
        output.append(col1)

    zbuffer = []
    for i in range(rows):
        col2 = []
        for j in range(col):
            col2.append(0)
        zbuffer.append(col2)

    for T in range(0, 628, 12):
        cosT, sinT = math.cos(T/100), math.sin(T/100)
        x2 = r2 + r1 * cosT #x coordinate 2D cricle
        y2 = r1 * sinT #y coordinate 2D circle

        for P in range(0, 628, 4):
            cosP, sinP = math.cos(P/100), math.sin(P/100)

            x = x2 * (cosB * cosP + sinA * sinB * sinP) - y2 * cosA * sinB
            y = x2 * (cosP * sinB - cosB * sinA * sinP) + y2 * cosA * cosB
            z = K2 + r1 * sinA * sinT + cosA * sinP * x2
            ooz = 1 / z

            xp = math.floor(-x * K1 * ooz)
            yp = math.floor(-y * K1 * ooz)

            l = cosP * cosT * sinB - cosA * cosT * sinP - sinA * sinT + cosB * (cosA * sinT - cosT * sinA * sinP)

            if l > -0.8:
                l = abs(l)
                yc = int((yp + y_offset) / y_space)
                xc = int((xp + x_offset) / x_space)

                if ooz > zbuffer[yc][xc]:
                    zbuffer[yc][xc] = ooz
                    L = round(l * 8)
                    output[yc][xc] = chars[L]

    for a in range(rows):
        for b in range(col):
            draw(b * x_space, a * y_space, output[a][b])


    if A > 6.283 and A < 6.2831:
        A = 0
        B = 0
    else:
        A += 0.006
        B += 0.006


    for event in pygame.event.get(): #close window when close button is pressed
        if event.type == QUIT:
            exit()

    pygame.display.update() #display changes