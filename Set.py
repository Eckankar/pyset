#!/usr/bin/python3.1
import pygame
from threading import Event
from Shape import Shape

WIDTH = 600
HEIGHT = 600
SLEEP = 0

def initDisplay():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    return window

def draw(window, cards):
    window.fill((0, 128, 0))
    for i in range(len(cards)):
        shape = cards[i]
        x, y = i//3, i%3
        shape.drawCard(window,
                       (x * 100 + 5, y * 140 + 5),
                       (85, 120))
    pygame.display.flip()

def main():
    window = initDisplay()
    cards = []
    for x in range(3):
        for y in range(3):
            cards.append(Shape(x, y+1, x, y))

    closeApp = False
    i = 0
    event = Event()
    while not closeApp:
        i += 1
        draw(window, cards)
        if SLEEP > 0:
            event.wait(SLEEP)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                closeApp = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c and e.mod & pygame.KMOD_CTRL != 0:
                    closeApp = True
                elif e.key == pygame.K_F4 and e.mod & pygame.KMOD_ALT != 0:
                    closeApp = True

if __name__ == '__main__':
    main()
