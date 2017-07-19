import time

from Chatroom import *


class ChatSystem:
    DEFAULT_CHATROOM = "general"
    def __init__(self):
        self.chatrooms = {self.DEFAULT_CHATROOM : Chatroom(self.DEFAULT_CHATROOM,None)}
        #get DBHandler


    def signup(self, username, password):
        self.__formatUsername(username)
        self.__formatPassword(password)

        return self.dbHandler.insert(username, password)


    def login(self, username, password):
        user = self.dbHandler.findByName(username)

        return user.id

    def addChatroom(self, ownerID, chatroomName):
        try:
            chatroom = self.__getChatroom(chatroomName)
            raise DuplicateChatroomException
        except ChatroomDoesNotExistException:
            pass

        owner = self.dbHandler.findByID(ownerID)

        self.chatrooms[chatroomName] = Chatroom(chatroomName, owner)


    def deleteChatroom(self, ownerName, chatroomName):
        chatroom = self.__getChatroom(chatroomName)

        owner = self.dbHandler.findByName(ownerName)

        if owner.id == chatroom.owner:
            self.chatrooms.pop(chatroomName)
        else:
            raise NotOwnerException

    def joinChatroom(self, roomName, username):
        chatroom = self.__getChatroom(roomName)

        user = self.dbHandler.findByName(username)

        chatroom.join(user)

    def addMessage(self, room, username, text):
        chatroom = self.__getChatroom(room)
        user = dbHandler.findByName(username)
        formattedMessage = self.__formatMessage(text)

        chatroom.addMessage(Message(username,formattedMessage,self.__getTime()))

    def getMessagesByTime(self, room, username):
        chatroom = self.__getChatroom(room)

        user = dbHandler.findByName(username)

        return chatroom.getMessagesByTime(self.getTime() - 60, user)

    def getMessagesByIndex(self, room, username, start):
        chatroom = self.__getChatroom(room)

        user = dbHandler.findByName(username)

        return chatroom.getMessagesByIndex(start, user)

    def banUser(self, ownerName, room, username):
        chatroom = self.__getChatroom(room)
        owner = dbHandler.findByName(ownerName)
        user = dbHandler.findByName(username)

        chatroom.banUser(owner, user)

    def unbanUser(self, owner, room, user):
        chatroom = self.__getChatroom(room)
        owner = dbHandler.findByName(ownerName)
        user = dbHandler.findByName(username)

        chatroom.unbanUser(owner, user)

    def __getChatroom(self, name):
        try:
            return self.chatrooms[name]
        except KeyError:
            raise ChatroomDoesNotExistException

    def __formatMessage(self, message):
        pass

    def __formatUsername(self, username):
        pass

    def __formatPassword(self, password):
        pass

    def __getTime(self):
        return int(time.time())

class ChatroomDoesNotExistException:
    pass

class DuplicateChatroomException:
    pass

class DuplicatUsernameException:
    pass

class UsernameFormatException:
    pass

class PasswordFormatException:
    pass

class UserNotFoundException:
    pass


