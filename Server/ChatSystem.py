import time
import re
from Chatroom import *
from DBHandler import *
from Message import Message


class ChatSystem:

    DEFAULT_CHATROOM = "general"
    def __init__(self):
        self.chatrooms = {self.DEFAULT_CHATROOM : Chatroom(self.DEFAULT_CHATROOM,None)}
        self.dbHandler = dbHandler
        self.userRE = re.compile('^[a-zA-Z0-9]{1,20}$')
        self.passwordRE = self.userRE
        self.chatroomRE = self.userRE


    # signs the user up to the ChatSystem
    # Input:
    #   username : str : Not None
    #   password : str : Not None
    # Returns:
    #   userID : int
    # Exceptions:
    #   DuplicateUsernameException
    #   GenericServerException
    #   UsernameFormatException
    #   PasswordFormatException
    def signup(self, username, password):
        self.__formatUsername(username)
        self.__formatPassword(password)

        try:
            userID = self.dbHandler.insert(username, password)
            return userID
        except DuplicateNameException:
            raise DuplicateUsernameException
        except DBException:
            raise GenericServerException


    # logs the user into the ChatSystem
    # Input:
    #   username : str : Not None
    #   password : str : Not None
    # Returns:
    #   userID : int
    # Exceptions:
    #   UserNotFoundException
    #   GenericServerException
    def login(self, username, password):
        #authentication is handled externally, so just return the username
        user = self.__getUserByName(username)
        return user.id

    # creates a new chatroom
    # Input:
    #   ownerID : int : Not None
    #   chatroomName : str : Not None
    # Exceptions:
    #   ChatroomFormatException
    #   DuplicateChatroomException
    #   UserNotFoundException
    #   GenericServerException
    def addChatroom(self, ownerID, chatroomName):
        try:
            chatroom = self.__getChatroom(chatroomName)
            raise DuplicateChatroomException
        except ChatroomDoesNotExistException:
            pass

        self.__formatChatroomName(chatroomName)

        owner = self.__getUserByID(ownerID)

        self.chatrooms[chatroomName] = Chatroom(chatroomName,owner)

    # deletes the chatroom, if authorized
    # Input:
    #   ownerID : int : Not None
    #   chatroomName : str : Not None
    # Exceptions:
    #   ChatroomDoesNotExistException
    #   UserNotFoundException
    #   GenericServerException
    #   NotOwnerException
    def deleteChatroom(self, ownerID, chatroomName):
        chatroom = self.__getChatroom(chatroomName)

        owner = self.__getUserByID(ownerID)

        if chatroom.owner and owner.id == chatroom.owner.id:
            self.chatrooms.pop(chatroomName)
        else:
            raise NotOwnerException

    # joins the chatroom
    # Input:
    #   roomName : str : Not None
    #   userID : int : Not None
    # Exceptions:
    #   ChatroomDoesNotExistException
    #   UserNotFoundException
    #   GenericServerException
    #   UserBannedException
    def joinChatroom(self, roomName, userID):
        chatroom = self.__getChatroom(roomName)

        user = self.__getUserByID(userID)

        chatroom.join(user)

    def set_alias(self, userID, newUsername, password):
        try:
            self.dbHandler.updateUser(userID, newUsername, password)
        except DuplicateNameException:
            raise DuplicateUsernameException
        except IDNotExistException:
            raise UserNotFoundException
        except DBException:
            raise GenericServerException

    # Adds Message to chatroom
    # Input:
    #   room : str : Not None
    #   userID : userID : Not None
    #   text : str : Not None
    # Exceptions:
    #   ChatroomDoesNotExistException
    #   UserNotFoundException
    #   GenericServerException
    #   MessageFormatException
    #   UserBannedException
    def addMessage(self, room, userID, text):
        chatroom = self.__getChatroom(room)

        user = self.__getUserByID(userID)
        formattedMessage = self.__formatMessage(text)

        chatroom.addMessage(Message(user,formattedMessage,self.__getTime()))

    # Gets a list of messages up to and including 60s ago
    # Input:
    #   roomName : str : Not None
    #   userID : int : Not None
    # Returns:
    #   ( idOfLastMessage : Int, [Message])
    # Exceptions:
    #   ChatroomDoesNotExistException
    #   UserNotFoundException
    #   GenericServerException
    #   UserBannedException
    def getMessagesByTime(self, roomName, userID):
        chatroom = self.__getChatroom(roomName)

        user = self.__getUserByID(userID)

        return chatroom.getMessagesByTime(self.__getTime() - 60, user)

    # get all messages with higher index than start
    # Input:
    #   roomName : str : Not None
    #   userID : int : Not None
    #   start : int : Nonable
    # Returns:
    #   [Message]
    # Exceptions:
    #   ChatroomDoesNotExistException
    #   UserNotFoundException
    #   GenericServerException
    #   UserBannedException
    def getMessagesByIndex(self, roomName, userID, start):
        chatroom = self.__getChatroom(roomName)

        user = self.__getUserByID(userID)

        if start is None:
            return chatroom.getMessagesByIndex(-1, user)
        else:
            return chatroom.getMessagesByIndex(start, user)

    # bans user from chatroom, if authorized
    # Input:
    #   ownerID : int : Not None
    #   roomName : str : Not None
    #   username : str : Not None
    # Exceptions:
    #   ChatroomDoesNotExistException
    #   UserNotFoundException
    #   GenericServerException
    #   NotOwnerException
    #   UserIsOwnerException
    def banUser(self, ownerID, roomName, username):
        chatroom = self.__getChatroom(roomName)

        owner = self.__getUserByID(ownerID)
        user = self.__getUserByName(username)

        chatroom.banUser(owner, user)

    # Unbans the user from the chatroom, if authorized
    # Input:
    #   ownerID : int : Not None
    #   roomName : str : Not None
    #   username : str : Not None
    # Exceptions:
    #   ChatroomDoesNotExistException
    #   UserNotFoundException
    #   GenericServerException
    #   NotOwnerException
    #   UserNotBannedException
    def unbanUser(self, ownerID, roomName, username):
        chatroom = self.__getChatroom(roomName)

        owner = self.__getUserByID(ownerID)
        user = self.__getUserByName(username)

        chatroom.unbanUser(owner, user)

    # returns the chatroom with the specified name
    # throws an exception if not found
    # Input:
    #   name : str : Not None
    # Returns:
    #   Chatroom
    # Exceptions:
    #   ChatrooomDoesNotExistException
    def __getChatroom(self, name):
        try:
            return self.chatrooms[name]
        except KeyError:
            raise ChatroomDoesNotExistException

    # returns a user from the database,
    # throws an exception if the user is not found or,
    # an exception happens while communicating with the database
    # Input:
    #   userID : int : Not None
    # returns:
    #   User
    # Exceptions:
    #   UserNotFoundException
    #   GenericServerException
    def __getUserByID(self, userID):
        try:
            user = self.dbHandler.findByID(userID)

            if user is None:
                raise UserNotFoundException
            else:
                return user
        except DBException:
            raise GenericServerException

    # returns a user from the database,
    # throws an exception if the user is not found or,
    # an exception happens while communicating with the database
    # Input:
    #   username : str : Not None
    # returns:
    #   User
    # Exceptions:
    #   UserNotFoundException
    #   GenericServerException
    def __getUserByName(self, username):
        try:
            user = self.dbHandler.findByName(username)

            if user is None:
                raise UserNotFoundException
            else:
                return user
        except DBException:
            raise GenericServerException

    # Checks the formatting of the message, truncates if too long
    # Input:
    #   message : str : Not None
    # Returns:
    #   formattedMessage : str
    # Exceptions:
    #   MessageFormatException
    def __formatMessage(self, message):
        if len(message) < 200:
            return message
        else:
            return message[:200]

    # Checks the formatting of the username, throws exception if there is a problem
    # Input:
    #   username : str : Not None
    # Exceptions:
    #   UsernameFormatException
    def __formatUsername(self, username):
        match = self.userRE.search(username)

        if match is None:
            raise UsernameFormatException

    # Checks the formatting of the password, throws exception if there is a problem
    # Input:
    #   password : str : Not None
    # Exceptions:
    #   PasswordFormatException
    def __formatPassword(self, password):
        match = self.passwordRE.search(password)

        if match is None:
            raise PasswordFormatException

    # Checks the formatting of the chatroom name, throws exception if there is a problem
    # Input:
    #   chatroomName : str : Not None
    # Exceptions:
    #   ChatroomFormatException
    def __formatChatroomName(self, chatroomName):
        match = self.chatroomRE.search(chatroomName)

        if match is None:
            raise ChatroomFormatException

    # gets the current time
    # Returns:
    #   time : int
    def __getTime(self):
        return int(time.time())

class ChatroomDoesNotExistException(Exception):
    pass

class DuplicateChatroomException(Exception):
    pass

class DuplicateUsernameException(Exception):
    pass

class ChatroomFormatException(Exception):
    pass

class MessageFormatException(Exception):
    pass

class UsernameFormatException(Exception):
    pass

class PasswordFormatException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class GenericServerException(Exception):
    pass


