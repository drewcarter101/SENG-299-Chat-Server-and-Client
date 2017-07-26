import threading
import time
from ServerWrapper import BlockedException, ChatroomDoesNotExistException

class MessageUpdater():

    __DELAY = .1

    def __init__(self, serverWrapper, clientStateInfo, Chat):
        self.serverWrapper = serverWrapper
        self.clientStateInfo = clientStateInfo
        self.chat = Chat
    
    def run(self):
        self.stop = False
        thread = threading.Thread(target=self.__getNewMessages)
        thread.start()
        self.lastUpdate = None
        self.lastChatroom = self.clientStateInfo.chatroom


    def __getNewMessages(self):
        while True:
            if self.stop:
                return
            try:
                chatroom = self.__getChatroom()

                if self.lastChatroom != chatroom:
                    self.lastUpdate = None

                userID = self.clientStateInfo.credentials.userID
                password = self.clientStateInfo.credentials.password

                (self.lastUpdate,messages) = self.serverWrapper.get(userID, password, chatroom, self.lastUpdate)

                if self.__sameChatroom(chatroom):
                    for message in messages:
                        print message
            except BlockedException, ChatroomDoesNotExistException:
                self.__exitChatroom()
            except:
                print 'An error has occured while attempting to retrieve messages'

            if self.stop:
                return

            self.lastChatroom = self.__getChatroom()
            time.sleep(self.__DELAY)

    def __sameChatroom(self,chatroom):
        return self.clientStateInfo.chatroom == chatroom

    def __exitChatroom(self):
        self.clientStateInfo.chatroom = self.chat.__GENERAL_CHATROOM

    def __getChatroom(self):
        return self.clientStateInfo.chatroom

    def quit(self):
        self.stop = True

