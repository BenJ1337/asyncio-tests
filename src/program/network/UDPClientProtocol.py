import logging
import time
import pprint
import json


class UDPClientProtocol:
    logger = logging.getLogger("iplogger")
    serverAvailable = False
    life = False
    index = 0

    def __init__(self, message, gameState):
        self.message = message
        self.transport = None
        self.gameState = gameState

    def connection_made(self, transport):
        self.transport = transport
        logging.info('Client: Connection with Server established')
        respObject = None
        if self.gameState == None:
            respObject = json.dumps({'stage': 'connecting'})
        else:
            respObject = json.dumps({'stage': 'start_game', 'name': 'Benni'})

        self.transport.sendto(respObject.encode())

    def datagram_received(self, data, addr):
        logging.info('%s: Daten vom Server empfangen', addr)

        reqObject = json.loads(data.decode())
        if reqObject['stage'] == 'connecting':
            if('socket' in reqObject):
                self.serverAvailable = True
        elif reqObject['stage'] == 'start_game':
            if self.gameState != None:
                if 'playerid' in reqObject:
                    self.gameState.addPlayer(
                        reqObject['playerid'], reqObject['name'] + ' (Client)', reqObject['position'])
                    self.gameState.setLocalPlayerId(reqObject['playerid'])
                    logging.info('Client: add Player (id: %s, name: %s) to Gamestate',
                                 reqObject['playerid'], reqObject['name'])
                else:
                    logging.error('Server hat keine Player id geschickt')
                    # self.transport.sendto(str(self.index).encode())
        elif reqObject['stage'] == 'update_game':
            # logging.info('Game Update from Server recieved. %s',
            #             reqObject['gamestate'])
            gameStateServer = json.loads(reqObject['gamestate'])
            for key, player in gameStateServer['players'].items():
                self.gameState.updatePlayerLocation(key, player)

    def connection_lost(self, exc):
        logging.info("Client: Connection closed.")
        self.transport.close()

    def error_received(self, exc):
        logging.info("Client: Error recieved. %s", exc)

    def isServerAvailable(self):
        return self.serverAvailable
