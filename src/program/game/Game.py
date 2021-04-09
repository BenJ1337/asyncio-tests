import sys
import pygame
import random
import pprint
import asyncio
import logging
from .objects.Player import Player


class Game:
    def __init__(self, controller):
        self.controller = controller
        print('build gui')

    async def startGame(self, myFuture):
        pygame.init()
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.controller.getScreenSize())

        run_game = True
        while run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False
                    # if event.key == pygame.K_ESCAPE:
                    #    run_game = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.controller.movePlayerUp()
                elif keys[pygame.K_s]:
                    self.controller.movePlayerDown()
                elif keys[pygame.K_a]:
                    self.controller.movePlayerLeft()
                elif keys[pygame.K_d]:
                    self.controller.movePlayerRight()

            self.screen.fill(self.black)
            self.controller.draw()

            pygame.display.update()
            await asyncio.sleep(.033)

        logging.info('Spiel geendet')
        myFuture.set_result(True)
