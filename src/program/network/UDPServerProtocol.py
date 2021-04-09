import logging
import pprint
import json
import random
from ..game.GameState import GameState
from ..game.objects.Player import Player


class UDPServerProtocol:
    """
        Communication between server and clients
        stages:
        # connecting
        # start_game
        # update_game
    """

    id = 0

    def __init__(self, gameState, clients):
        self.gameState = gameState
        self.clients = clients

    def connection_made(self, transport):
        self.transport = transport
        pprint.pprint('Server ????!')

    def datagram_received(self, data, addr):
        logging.info('recieved data from client: %s', data.decode())
        logging.info(addr[0])
        if(addr[0] not in self.clients.keys()):
            self.clients[addr[0]] = addr

        reqObject = json.loads(data.decode())

        if reqObject['stage'] == 'connecting':
            dataRespObj = json.dumps(
                {'stage': 'connecting', 'socket': str(self.transport)})
            self.transport.sendto(dataRespObj.encode(), addr)

        elif reqObject['stage'] == 'start_game':
            id = UDPServerProtocol.id
            UDPServerProtocol.id += 1

            position = {
                'x': random.randint(0, GameState.width - Player.player_width),
                'y': random.randint(0, GameState.height - Player.player_width)
            }

            dataRespObj = json.dumps(
                {'stage': 'start_game', 'playerid': str(id), 'name': reqObject['name'], 'position': position})
            self.transport.sendto(dataRespObj.encode(), addr)
            logging.info('Server: add Player (id: %s, name: %s)',
                         str(id), reqObject['name'])

            self.gameState.addPlayer(
                str(id), reqObject['name'] + ' (Server)', position)

            UDPServerProtocol.id += 1
        elif reqObject['stage'] == 'update_game' and reqObject['action'] == 'movePlayer':
            if reqObject['playerid'] in self.gameState.players:
                self.gameState\
                    .players[reqObject['playerid']]\
                    .move(reqObject['direction'])
                logging.info(self.gameState.players[reqObject['playerid']])
            else:
                logging.error('Player with id %s not found',
                              reqObject['playerid'])

    def connection_lost(self, exc):
        print("Server: Connection lost: ", exc)
