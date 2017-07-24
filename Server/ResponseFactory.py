import json


class ResponseFactory:

    __RESPONSE_TYPE = 'responseType'
    __REQUEST_TYPE_MISSING = 'RequestTypeMissing'
    __REQUEST_FORMAT_ERROR = 'RequestFormatError'
    __PARAMETER_FORMAT_ERROR = 'ParameterFormatError'
    __OK = 'Ok'
    __DUPLICATE_USERNAME = 'DuplicateUsername'
    __INVALID_USERNAME = 'InvalidUsername'
    __INVALID_PASSWORD = 'InvalidPassword'
    __PARAMETERS_MISSING = 'ParametersMissing'
    __INVALID_CREDENTIALS = 'InvalidCredentials'
    __INVALID_MESSAGE = 'InvalidMessage'
    __BLOCKED = 'Blocked'
    __CHATROOM_DOES_NOT_EXIST = 'ChatroomDoesNotExist'
    __LAST_UPDATE = 'lastUpdate'
    __MESSAGES = 'messages'
    __DUPLICATE_CHATROOM = 'DuplicateChatroom'
    __USER_DOES_NOT_EXIST = 'UserDoesNotExist'
    __NOT_OWNER = 'NotOwner'
    __USER_NOT_ON_LIST = 'UserNotOnList'
    __USERNAME = 'username'
    __TEXT = 'text'
    __USER_ID = 'userID'

    def __init__(self):
        pass

    def ok(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__OK})

    def requestTypeMissing(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__REQUEST_TYPE_MISSING})

    def requestFormatError(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__REQUEST_FORMAT_ERROR})

    def duplicateUsername(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__DUPLICATE_USERNAME})

    def invalidUsername(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__INVALID_USERNAME})

    def invalidPassword(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__INVALID_PASSWORD})

    def parametersMissing(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__PARAMETERS_MISSING})

    def invalidCredentials(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__INVALID_CREDENTIALS})

    def invalidMessage(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__INVALID_MESSAGE})

    def blocked(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__BLOCKED})

    def chatroomDoesNotExist(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__CHATROOM_DOES_NOT_EXIST})

    def duplicateChatrooom(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__DUPLICATE_CHATROOM})

    def userDoesNotExist(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__USER_DOES_NOT_EXIST})

    def notOwner(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__NOT_OWNER})

    def userNotOnList(self):
        return json.dumps({self.__RESPONSE_TYPE : self.__USER_NOT_ON_LIST})

    def returnMessages(self, lastUpdate, messages):
        response = {self.__RESPONSE_TYPE : self.__OK, self.__LAST_UPDATE : lastUpdate}
        messagesList = []
        for message in messages:
            messagesList.append({self.__USERNAME : message.user.name, self.__TEXT : message.text})

        response[self.__MESSAGES] = messagesList
        return json.dumps(response)

    def loggedIn(self, userID):
        return json.dumps({self.__RESPONSE_TYPE : self.__OK, self.__USER_ID : userID})

    def parameterFormatError(self):
        return json.dumps({self.__RESPONSE_TYPE: self.__PARAMETER_FORMAT_ERROR})

