import asyncio
import logging
from .NetworkConfig import NetworkConfig
from .UDPClientProtocol import UDPClientProtocol


class Client:
    def __init__(self, gameState):
        self.gameState = gameState

    def testServer(self):
        return asyncio.run(self.mainTestServer())

    async def connect2Server(self, myFuture):
        logging.info('Connect 2 Server')

        message = 'hello Server'
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UDPClientProtocol(
                message, self.gameState),
            remote_addr=NetworkConfig.serverSocket)

        self.transport = transport

        try:
            print('Client is running')
            await myFuture
            print('shut down client')
        finally:
            transport.close()

        return True

    async def mainTestServer(self):
        return await self.checkServerIsOnline()

    async def checkServerIsOnline(self):
        loop = asyncio.get_running_loop()

        on_con_lost = loop.create_future()
        message = "server present?"

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UDPClientProtocol(message, None),
            remote_addr=NetworkConfig.serverSocket)

        try:
            await asyncio.sleep(0.1)
        finally:
            transport.close()

        return protocol.isServerAvailable()
