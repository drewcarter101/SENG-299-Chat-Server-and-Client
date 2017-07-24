import json
from ResponseFactory import ResponseFactory
import socket
from Controller import Controller


class Server:
    PORT = 9321

    #Parameter Names
    REQUEST_TYPE = 'requestType'
    USERNAME = 'username'
    PASSWORD = 'password'
    USER_ID = 'userID'
    CHATROOM = 'chatroom'
    MESSAGE = 'message'
    LAST_UPDATE = 'lastUpdate'
    NEW_USERNAME = 'newUsername'
    USER_TO_BLOCK = 'userToBlock'
    USER_TO_UNBLOCK = 'userToUnblock'

    #Request Types
    SIGN_UP = 'signup'
    LOGIN = 'login'
    SEND = 'send'
    GET = 'get'
    SET_ALIAS = 'set_alias'
    JOIN = 'join'
    CREATE = 'create'
    BLOCK = 'block'
    UNBLOCK = 'unblock'
    DELETE = 'delete'

    def __init__(self):
        self.responseFactory = ResponseFactory()
        self.controller = Controller()

    def start(self):
        s = socket.socket()
        host = socket.gethostname()

        s.bind((host,self.PORT))
        s.listen(100)

        while True:
            client, clientAddress = s.accept()

            request = client.recv(2048)

            response = self.__parseRequest(request)

            client.send(response)

    def __parseRequest(self, request):
        if not isinstance(request,str):
            return self.responseFactory.requestFormatError()

        try:
            requestDict = json.loads(request)
        except ValueError:
            return self.responseFactory.requestFormatError()

        try:
            requestType = requestDict[self.REQUEST_TYPE]
        except KeyError:
            return self.responseFactory.requestTypeMissing()

        #route the request to the proper function in the controller
        try:
            if requestType == self.SIGN_UP:
                username = self.__getParameter(requestDict, self.USERNAME, basestring, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                return self.controller.signup(username, password)
            elif requestType == self.LOGIN:
                username = self.__getParameter(requestDict, self.USERNAME, basestring, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                return self.controller.login(username, password)
            elif requestType == self.SEND:
                userID = self.__getParameter(requestDict, self.USER_ID, int, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                chatroom = self.__getParameter(requestDict, self.CHATROOM, basestring, False)
                message = self.__getParameter(requestDict, self.MESSAGE, basestring, False)
                return self.controller.send(userID, password, chatroom, message)
            elif requestType == self.GET:
                userID = self.__getParameter(requestDict, self.USER_ID, int, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                chatroom = self.__getParameter(requestDict, self.CHATROOM, basestring, False)
                lastUpdate = self.__getParameter(requestDict, self.LAST_UPDATE, int, True)
                return self.controller.get(userID, password, chatroom, lastUpdate)
            elif requestType == self.SET_ALIAS:
                userID = self.__getParameter(requestDict, self.USER_ID, int, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                newUsername = self.__getParameter(requestDict, self.NEW_USERNAME, basestring, False)
                return self.controller.set_alias(userID, password, newUsername)
            elif requestType == self.JOIN:
                userID = self.__getParameter(requestDict, self.USER_ID, int, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                chatroom = self.__getParameter(requestDict, self.CHATROOM, basestring, False)
                return self.controller.join(userID, password, chatroom)
            elif requestType == self.CREATE:
                userID = self.__getParameter(requestDict, self.USER_ID, int, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                chatroom = self.__getParameter(requestDict, self.CHATROOM, basestring, False)
                return self.controller.create(userID, password, chatroom)
            elif requestType == self.BLOCK:
                userID = self.__getParameter(requestDict, self.USER_ID, int, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                chatroom = self.__getParameter(requestDict, self.CHATROOM, basestring, False)
                userToBlock = self.__getParameter(requestDict, self.USER_TO_BLOCK, basestring, False)
                return self.controller.block(userID, password, chatroom, userToBlock)
            elif requestType == self.UNBLOCK:
                userID = self.__getParameter(requestDict, self.USER_ID, int, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                chatroom = self.__getParameter(requestDict, self.CHATROOM, basestring, False)
                userToUnblock = self.__getParameter(requestDict, self.USER_TO_UNBLOCK, basestring, False)
                return self.controller.unblock(userID, password, chatroom, userToUnblock)
            elif requestType == self.DELETE:
                userID = self.__getParameter(requestDict, self.USER_ID, int, False)
                password = self.__getParameter(requestDict, self.PASSWORD, basestring, False)
                chatroom = self.__getParameter(requestDict, self.CHATROOM, basestring, False)
                return self.controller.delete(userID, password, chatroom)
            else:
                return self.responseFactory.requestFormatError()
        except ParameterFormatException:
            return self.responseFactory.requestFormatError()
        except ParameterMissingException:
            return self.responseFactory.parametersMissing()


    def __getParameter(self,requestDict, key, type, nullable):
        try:
            value = requestDict[key]

            if isinstance(value, type):
                return value
            else:
                raise ParameterFormatException
        except KeyError:
            if not nullable:
                raise ParameterMissingException

        return None

class ParameterFormatException(Exception):
    pass

class ParameterMissingException(Exception):
    pass

server = Server()
server.start()