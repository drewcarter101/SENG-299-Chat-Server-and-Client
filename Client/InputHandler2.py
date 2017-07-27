import threading
import sys
from ServerWrapper import *


class InputHandler:

    def __init__(self, serverWrapper, clientStateInfo, Chat):
        self.serverWrapper = serverWrapper
        self.clientStateInfo = clientStateInfo
        self.chat = Chat

    def run(self):
        self.stop = False
        self.lastUpdate = None
        self.lastChatroom = self.clientStateInfo.chatroom
        self.thread = threading.Thread(target=self.__handleInput)

        #allows the program to close regardless of it this thread is running
        self.thread.daemon = True
        self.thread.start()

    def __handleInput(self):
        while True:
            input = raw_input()

    def quit(self):
        #couldn't find an elegant solution to interuptting the thread
        sys.exit()