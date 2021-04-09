from .GameState import GameState
import logging
import json


class Controller:
    def __init__(self, gameState, client):
        self.gameState = gameState
        self.client = client

    def getScreenSize(self):
        return GameState.screenSize

    def movePlayerUp(self):
        if self.gameState.localPlayerId in self.gameState.players:
            logging.info('Up')
            data = json.dumps(
                {'stage': 'update_game', 'action': 'movePlayer', 'direction': 'Up', 'playerid': self.gameState.localPlayerId})
            self.client.transport.sendto(data.encode())

    def movePlayerDown(self):
        if self.gameState.localPlayerId in self.gameState.players:
            logging.info('Down')
            data = json.dumps(
                {'stage': 'update_game', 'action': 'movePlayer', 'direction': 'Down', 'playerid': self.gameState.localPlayerId})
            self.client.transport.sendto(data.encode())

    def movePlayerLeft(self):
        if self.gameState.localPlayerId in self.gameState.players:
            logging.info('Left')
            data = json.dumps(
                {'stage': 'update_game', 'action': 'movePlayer', 'direction': 'Left', 'playerid': self.gameState.localPlayerId})
            self.client.transport.sendto(data.encode())

    def movePlayerRight(self):
        if self.gameState.localPlayerId in self.gameState.players:
            logging.info('Right')
            data = json.dumps(
                {'stage': 'update_game', 'action': 'movePlayer', 'direction': 'Right', 'playerid': self.gameState.localPlayerId})
            self.client.transport.sendto(data.encode())

    def draw(self):
        for key, player in self.gameState.players.items():
            player.draw()
