import unittest
from ResponseFactory import ResponseFactory
from Message import Message

class ResponseFactoryTest (unittest.TestCase):
    def testOK(self):
        responseFactory = ResponseFactory()
        response = responseFactory.ok()
        self.assertEqual(response,'{"responseType": "Ok"}')

    def testRequestTypeMissing(self):
        responseFactory = ResponseFactory()
        response = responseFactory.requestTypeMissing()
        self.assertEqual(response, '{"responseType": "RequestTypeMissing"}')

    def testRequestFormatError(self):
        responseFactory = ResponseFactory()
        response = responseFactory.requestFormatError()
        self.assertEqual(response, '{"responseType": "RequestFormatError"}')

    def testDuplicateUsername(self):
        responseFactory = ResponseFactory()
        response = responseFactory.duplicateUsername()
        self.assertEqual(response, '{"responseType": "DuplicateUsername"}')

    def testInvalidUsername(self):
        responseFactory = ResponseFactory()
        response = responseFactory.invalidUsername()
        self.assertEqual(response, '{"responseType": "InvalidUsername"}')

    def testInvalidPassword(self):
        responseFactory = ResponseFactory()
        response = responseFactory.invalidPassword()
        self.assertEqual(response, '{"responseType": "InvalidPassword"}')

    def testParametersMissing(self):
        responseFactory = ResponseFactory()
        response = responseFactory.parametersMissing()
        self.assertEqual(response, '{"responseType": "ParametersMissing"}')

    def testInvalidCredentials(self):
        responseFactory = ResponseFactory()
        response = responseFactory.invalidCredentials()
        self.assertEqual(response, '{"responseType": "InvalidCredentials"}')

    def testInvalidMessage(self):
        responseFactory = ResponseFactory()
        response = responseFactory.invalidMessage()
        self.assertEqual(response, '{"responseType": "InvalidMessage"}')

    def testBlocked(self):
        responseFactory = ResponseFactory()
        response = responseFactory.blocked()
        self.assertEqual(response, '{"responseType": "Blocked"}')

    def testChatroomDoesNotExist(self):
        responseFactory = ResponseFactory()
        response = responseFactory.chatroomDoesNotExist()
        self.assertEqual(response, '{"responseType": "ChatroomDoesNotExist"}')

    def testDuplicateChatroom(self):
        responseFactory = ResponseFactory()
        response = responseFactory.duplicateChatrooom()
        self.assertEqual(response, '{"responseType": "DuplicateChatroom"}')

    def testUserDoesNotExist(self):
        responseFactory = ResponseFactory()
        response = responseFactory.userDoesNotExist()
        self.assertEqual(response, '{"responseType": "UserDoesNotExist"}')

    def testNotOwner(self):
        responseFactory = ResponseFactory()
        response = responseFactory.notOwner()
        self.assertEqual(response, '{"responseType": "NotOwner"}')

    def testUserNotOnList(self):
        responseFactory = ResponseFactory()
        response = responseFactory.userNotOnList()
        self.assertEqual(response, '{"responseType": "UserNotOnList"}')

    def testParameterFormatError(self):
        responseFactory = ResponseFactory()
        response = responseFactory.parameterFormatError()
        self.assertEqual(response, '{"responseType": "ParameterFormatError"}')

    def testLoggedIn(self):
        responseFactory = ResponseFactory()
        response = responseFactory.loggedIn(132)
        self.assertEqual(response, '{"responseType": "Ok", "userID": 132}')

    def testReturnMessages(self):
        responseFactory = ResponseFactory()
        messages = [Message('cam','text',456)]
        response = responseFactory.returnMessages(123, messages)
        self.assertEqual(response, '{"responseType": "Ok", "messages": [{"username": "cam", "text": "text"}], "lastUpdate": 123}')

    def testReturnMessagesEmpty(self):
        responseFactory = ResponseFactory()
        messages = []
        response = responseFactory.returnMessages(12, messages)
        self.assertEqual(response, '{"responseType": "Ok", "messages": [], "lastUpdate": 12}')


unittest.main()