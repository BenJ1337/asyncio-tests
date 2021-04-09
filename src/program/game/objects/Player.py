import pygame
import random
import json
import logging
from .Point import Point


class Player(Point):
    color = 255, 255, 255
    player_width = 20
    speed = 2
    name = 'Player'

    def __init__(self, position, color, name):
        super().__init__(position['x'], position['y'])
        self.color = color
        self.name = name

    def __repr__(self):
        return 'Player: {} (x: {}, y: {})'.format(self.name, self.x, self.y)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def up(self):
        self.update_y(-1)

    def down(self):
        self.update_y(1)

    def right(self):
        self.update_x(1)

    def left(self):
        self.update_x(-1)

    def move(self, direction):
        logging.info('Move Player (%s) in Direction: %s', self.name, direction)
        if 'Up' == direction:
            self.up()
        if 'Down' == direction:
            self.down()
        if 'Right' == direction:
            self.right()
        if 'Left' == direction:
            self.left()

    def update_x(self, direction):
        screen = pygame.display.get_surface()
        newPosition = self.x + (self.speed * direction)
        if (direction > 0 and newPosition + self.player_width < screen.get_width()) or (direction < 0 and newPosition > 0):
            self.x = newPosition

    def update_y(self, direction):
        screen = pygame.display.get_surface()
        newPosition = self.y + (self.speed * direction)
        if (direction > 0 and newPosition + self.player_width < screen.get_height()) or (direction < 0 and newPosition > 0):
            self.y = newPosition

    def draw(self):
        font = pygame.font.SysFont("Arial", 12)
        screen = pygame.display.get_surface()

        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (self.x + self.player_width /
                    2 - text.get_width() / 2, self.y - 20))
        pygame.draw.rect(screen, self.color, pygame.Rect(
            self.x, self.y, self.player_width, self.player_width))
