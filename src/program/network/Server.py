import asyncio
import logging
import traceback
import json
from .NetworkConfig import NetworkConfig
from .UDPServerProtocol import UDPServerProtocol
from asyncio.exceptions import CancelledError


class Server:
    def __init__(self, gameState):
        self.gameState = gameState
        self.clients = {}

    async def runServer(self, myFuture):
        logging.info('State Server')

        loop = asyncio.get_running_loop()
        self.transport, protocol = await loop.create_datagram_endpoint(
            lambda: UDPServerProtocol(self.gameState, self.clients),
            local_addr=NetworkConfig.serverSocket)

        self.gameStateCached = ''
        try:
            logging.info('Server is running')
            while not myFuture.done():
                #logging.info('Clients: %s', len(self.clients))
                dataRespObj = json.dumps(
                    {'stage': 'update_game', 'gamestate': self.gameState.toJson()})
                if self.gameStateCached != dataRespObj:
                    self.gameStateCached = dataRespObj

                    for key, value in self.clients.items():
                        logging.info(
                            'distribute gamestate to client: %s:%s', key, value)
                        self.transport.sendto(dataRespObj.encode(), value)

                await asyncio.sleep(.033)
            logging.info('Server stopped')
        except CancelledError as ex:
            logging.info(ex)
        except:
            logging.info(traceback.format_exc())
        finally:
            print('Server stopped')
            self.transport.close()
