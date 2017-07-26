#!/usr/bin/env python
from MessageUpdater import MessageUpdater
from InputHandler import InputHandler
from ClientStateInfo import ClientStateInfo

class Chat:
    __GENERAL_CHATROOM = 'general'

    def __init__(self, credentials, serverWrapper):
        clientStateInfo = ClientStateInfo(credentials,self.__GENERAL_CHATROOM)
        self.messageUpdater = MessageUpdater(serverWrapper, clientStateInfo)
        self.inputHandler = InputHandler(serverWrapper, clientStateInfo)

    def run(self):
        self.messageUpdater.run()
        self.inputHandler.run()

    def quit(self):
        self.messageUpdater.quit()
        self.inputHandler.quit()
