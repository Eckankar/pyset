#!/usr/bin/python3.1
import pygame
from math import pi, sin, cos

class Shape():
    # Shape
    CIRCLE = 0
    DIAMOND = 1
    SQUIGGLY = 2

    # Color
    RED = 0
    GREEN = 1
    BLUE = 2

    # Fill
    EMPTY = 0
    STRIPED = 1
    SOLID = 2

    def __init__(self, shape, amount, color, fill):
        self.shape = shape
        self.amount = amount

        if color == Shape.RED:
            self.color = (255, 0, 0)
        elif color == Shape.GREEN:
            self.color = (0, 255, 0)
        else:
            self.color = (0, 0, 255)

        self.fill = fill

    def drawStripes(self, window, topleft, dimensions):
        (x, y) = topleft
        (dx, dy) = dimensions

        numStripes = 18

        stripeWidth = int(dx / (2*numStripes-1))

        leftDiff = dx / numStripes
        left = x + leftDiff / 2

        for i in range(numStripes):
            pygame.draw.line(window, (255, 255, 255),
                                     (left, y), (left, y+dy), stripeWidth)
            left += leftDiff

    def drawArc(self, window, rect, start, end, outline):
        pygame.draw.arc(window, self.color, rect, start, end, outline)

    def drawSymbol(self, window, topleft, dimensions, filled):
        (x, y) = topleft
        (dx, dy) = dimensions

        if filled:
            outline = 0
        else:
            outline = 3

        if self.shape == Shape.CIRCLE:
            arcPercent = 0.2
            if filled:
                pygame.draw.rect(window, self.color,
                                (x + arcPercent * dx, y,
                                dx * (1 - 2*arcPercent), dy))
                pygame.draw.ellipse(window, self.color,
                                    (x, y, 2*arcPercent*dx, dy), outline)
                pygame.draw.ellipse(window, self.color, (x+dx-2*arcPercent*dx, y,
                                    2*arcPercent*dx, dy), outline)
            else:
                pygame.draw.line(window, self.color, (x+arcPercent*dx, y+outline/2),
                                    (x+dx-arcPercent*dx, y+outline/2), outline)
                pygame.draw.line(window, self.color,
                                 (x+arcPercent*dx, y+dy-outline/2),
                                 (x+dx-arcPercent*dx, y+dy-outline/2), outline)
                pygame.draw.arc(window, self.color,
                                    (x, y, 2*arcPercent*dx, dy),
                                    pi/2, 3*pi/2, outline)
                pygame.draw.arc(window, self.color, (x+dx-2*arcPercent*dx, y,
                                    2*arcPercent*dx, dy), 3*pi/2, 5*pi/2, outline)

        elif self.shape == Shape.DIAMOND:
            midX = x + dx/2
            midY = y + dy/2
            pygame.draw.polygon(window, self.color, [
                (x, midY), (midX, y), (x+dx, midY), (midX, y+dy)
            ], outline)
        elif self.shape == Shape.SQUIGGLY:
            xx = dx/8
            yy = dy/5
            o = outline

            def drange(start,stop, step):
                    r = start
                    if stop < start:
                        step = -step
                    while ((start < stop and r < stop) or
                           (start > stop and r > stop)):
                            yield r
                            r += step

            def arcToPoints(rect, start, end):
                (x, y, dx, dy) = rect
                dx, dy = dx/2, dy/2
                midX, midY = x+dx, y+dy

                points = []
                for i in drange(start, end, 0.03):
                    points.append((
                        midX + cos(i) * dx,
                        midY - sin(i) * dy
                    ))

                return points

            pointLists = [
                arcToPoints((0, 3.5, 1, 1),     pi, 2*pi),
                arcToPoints((1,   3, 3, 2),     pi,    0),
                arcToPoints((4,   3, 3, 2),     pi, 2*pi),
                arcToPoints((6,  -2, 2, 6), 3*pi/2, 2*pi),
                arcToPoints((7, 0.5, 1, 1),      0,   pi),
                arcToPoints((4,   0, 3, 2),   2*pi,   pi),
                arcToPoints((1,   0, 3, 2),      0,   pi),
                arcToPoints((0,   1, 2, 6),   pi/2,   pi),
            ]

            points = []
            for ls in pointLists:
                points.extend(ls)

            for i in range(len(points)):
                (cx, cy) = points[i]
                points[i] = (x+cx*xx, y+cy*yy)


            pygame.draw.polygon(window, self.color, points, o)
        else:
            pygame.draw.rect(window, self.color, (x, y, dx, dy))

    def drawCard(self, window, topleft, dimensions):
        (x, y) = topleft
        (dx, dy) = dimensions
        pygame.draw.rect(window, (255, 255, 255), (x, y, dx, dy))
        pygame.draw.rect(window, (0, 0, 0), (x, y, dx, dy), 1)

        # Size of symbols
        sw = 0.85 * dx
        sh = 0.25 * dy

        # Top of first symbol
        topDiff = dy / self.amount
        top = y + topDiff / 2 - sh / 2

        # Left of symbols
        left = x + (dx - sw)/2

        for i in range(self.amount):
            if self.fill != Shape.EMPTY:
                self.drawSymbol(window, (left, top), (sw, sh), True)
            if self.fill == Shape.STRIPED:
                self.drawStripes(window, (left, top), (sw, sh))
            if self.fill != Shape.SOLID:
                self.drawSymbol(window, (left, top), (sw, sh), False)
            top += topDiff
