from .objects.Player import Player
import random
import pygame
import json
import logging


class GameState:
    screenSize = width, height = 1000, 500

    def __init__(self, server):
        self.players = {}

    def setLocalPlayerId(self, id):
        self.localPlayerId = id

    def addPlayer(self, id, name, position):
        self.players[id] = Player(position,
                                  (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), name)
        print('> players: ' + str(len(self.players)))

    def updatePlayerLocation(self, key, player):
        #logging.info('Player: %s', player)
        self.players[key].x = player['x']
        self.players[key].y = player['y']

    def __repr__(self):
        result = '{\'player\':{'
        for key, player in self.players:
            result += str(key) + ':' + player
        result += '}}'
        return result

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
