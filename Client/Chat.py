#!/usr/bin/env python
from MessageUpdater import MessageUpdater
from InputHandler import InputHandler
from ClientStateInfo import ClientStateInfo
from Constant import GENERAL_CHATROOM

class Chat:

    def __init__(self, credentials, serverWrapper):
        clientStateInfo = ClientStateInfo(credentials,GENERAL_CHATROOM)
        self.messageUpdater = MessageUpdater(serverWrapper, clientStateInfo, self)
        self.inputHandler = InputHandler(serverWrapper, clientStateInfo, self)

    def run(self):
        self.messageUpdater.run()
        self.inputHandler.run()

    def quit(self):
        self.messageUpdater.quit()
        self.inputHandler.quit()
