import json


class ResponseFactory:

    RESPONSE_TYPE = 'responseType'
    REQUEST_TYPE_MISSING = 'RequestTypeMissing'
    REQUEST_FORMAT_ERROR = 'RequestFormatError'
    PARAMETER_FORMAT_ERROR = 'ParameterFormatError'
    OK = 'Ok'
    DUPLICATE_USERNAME = 'DuplicateUsername'
    INVALID_USERNAME = 'InvalidUsername'
    INVALID_PASSWORD = 'InvalidPassword'
    PARAMETERS_MISSING = 'ParametersMissing'
    INVALID_CREDENTIALS = 'InvalidCredentials'
    INVALID_MESSAGE = 'InvalidMessage'
    BLOCKED = 'Blocked'
    CHATROOM_DOES_NOT_EXIST = 'ChatroomDoesNotExist'
    LAST_UPDATE = 'lastUpdate'
    MESSAGES = 'messages'
    DUPLICATE_CHATROOM = 'DuplicateChatroom'
    USER_DOES_NOT_EXIST = 'UserDoesNotExist'
    NOT_OWNER = 'NotOwner'
    USER_NOT_ON_LIST = 'UserNotOnList'
    USERNAME = 'username'
    TEXT = 'text'
    USER_ID = 'userID'

    def __init__(self):
        pass

    def ok(self):
        return json.dumps({self.RESPONSE_TYPE : self.OK})

    def requestTypeMissing(self):
        return json.dumps({self.RESPONSE_TYPE : self.REQUEST_TYPE_MISSING})

    def requestFormatError(self):
        return json.dumps({self.RESPONSE_TYPE : self.REQUEST_FORMAT_ERROR})

    def duplicateUsername(self):
        return json.dumps({self.RESPONSE_TYPE : self.DUPLICATE_USERNAME})

    def invalidUsername(self):
        return json.dumps({self.RESPONSE_TYPE : self.INVALID_USERNAME})

    def invalidPassword(self):
        return json.dumps({self.RESPONSE_TYPE : self.INVALID_PASSWORD})

    def parametersMissing(self):
        return json.dumps({self.RESPONSE_TYPE : self.PARAMETERS_MISSING})

    def invalidCredentials(self):
        return json.dumps({self.RESPONSE_TYPE : self.INVALID_CREDENTIALS})

    def invalidMessage(self):
        return json.dumps({self.RESPONSE_TYPE : self.INVALID_MESSAGE})

    def blocked(self):
        return json.dumps({self.RESPONSE_TYPE : self.BLOCKED})

    def chatroomDoesNotExist(self):
        return json.dumps({self.RESPONSE_TYPE : self.CHATROOM_DOES_NOT_EXIST})

    def duplicateChatrooom(self):
        return json.dumps({self.RESPONSE_TYPE : self.DUPLICATE_CHATROOM})

    def userDoesNotExist(self):
        return json.dumps({self.RESPONSE_TYPE : self.USER_DOES_NOT_EXIST})

    def notOwner(self):
        return json.dumps({self.RESPONSE_TYPE : self.NOT_OWNER})

    def userNotOnList(self):
        return json.dumps({self.RESPONSE_TYPE : self.USER_NOT_ON_LIST})

    def returnMessages(self, lastUpdate, messages):
        response = {self.RESPONSE_TYPE : self.OK, self.LAST_UPDATE : lastUpdate}
        messagesList = []
        for message in messages:
            messagesList.append({self.USERNAME : message.user.name, self.TEXT : message.text})

        response[self.MESSAGES] = messagesList
        return json.dumps(response)

    def loggedIn(self, userID):
        return json.dumps({self.RESPONSE_TYPE : self.OK, self.USER_ID : userID})

    def parameterFormatError(self):
        return json.dumps({self.RESPONSE_TYPE: self.PARAMETER_FORMAT_ERROR})