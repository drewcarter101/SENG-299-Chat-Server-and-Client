from Authenticator import Authenticator
from ChatSystem import ChatSystem
from ResponseFactory import ResponseFactory


class Controller:
    def __init__(self):
        self.authenticator = Authenticator()
        self.chatSystem = ChatSystem()
        self.responseFactory = ResponseFactory()

    #These functions deal with routing the requests to the proper ChatSystem functions,
    #They assume that all parameters are not None, unless otherwise specified and the
    #parameters are of the proper type
    #The functions return a string corresponding to the proper response type
    #The functions authenticate the users if necessary
    def login(self, username, password):
        if not authenticator.authenticateByName(username, password):
            return self.responseFactory.invalidCredentials()

        userID = self.chatSystem.login(username, password)

        if userID:
            return self.responseFactory.loggedin(userID)
        else:
            return self.responseFactory.invalidCredentials()

    def signup(self, username, password):
        try:
            self.chatSystem.signup(username, password)
        except:
            pass

    def send(self, userID, password, chatroom, message):
        pass

    def get(self, userID, password, chatroom, lastUpdate):
        pass

    def set_alias(self, userID, password, newUsername):
        pass

    def join(self, userID, password, chatroom):
        pass

    def create(self, userID, password, chatroom):
        pass

    def delete(self, userID, password, chatroom):
        pass

    def block(self, userID, password, chatroom, userToBlock):
        pass

    def unblock(self, userID, password, chatroom, userToUnblock):
        pass



