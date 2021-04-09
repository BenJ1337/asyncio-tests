#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from program.network.Server import Server
from program.network.Client import Client
from program.game.Game import Game
from program.game.Controller import Controller
from program.game.GameState import GameState

server = None
client = None


async def createNewServer(game):
    logging.info('Start server and connect to it')
    loop = asyncio.get_running_loop()
    myFuture = loop.create_future()
    setupServerAysnc = asyncio.create_task(server.runServer(myFuture))

    await asyncio.sleep(0.3)

    setupClientAysnc = asyncio.create_task(client.connect2Server(myFuture))
    setupGameAysnc = asyncio.create_task(game.startGame(myFuture))
    await setupServerAysnc
    await setupClientAysnc
    await setupGameAysnc

if "__main__" == __name__:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%d.%m.%Y %H:%M:%S >')

    logging.info("start programm")

    server = Server(GameState(''))
    gameState = GameState('player1')
    client = Client(gameState)

    controller = Controller(gameState, client)
    game = Game(controller)

    serverAvailable = client.testServer()
    print('Server available: ' + str(serverAvailable))
    try:
        if not serverAvailable:
            asyncio.run(createNewServer(game))
        else:
            asyncio.run(client.connect2Server())
    except KeyboardInterrupt:
        logging.info('Programm per STRG + C beendet')

    logging.info("end programm")
