import unittest
import json
from DBHandler import dbHandler
from Controller import Controller
import time


class ControllerTest(unittest.TestCase):
    def setUp(self):
        dbHandler.usersByName = {}
        dbHandler.usersByID = {}

    def testSignupAndLogin(self):
        controller = Controller()

        username = 'cam'
        password = 'password'

        signupResponse = controller.signup(username, password)

        signupID = self.getID(signupResponse)

        loginResponse = controller.login(username, password)

        loginID = self.getID(loginResponse)
        self.assertEqual(loginID, signupID)

    def testSignupExceptions(self):
        controller = Controller()

        username = 'cam'
        password = 'password'

        controller.signup(username, password)

        self.assertDuplicateUsername(controller.signup(username, password))
        self.assertUsernameFormatError(controller.signup("",password))
        self.assertUsernameFormatError(controller.signup("aaaaaaaaaaaaaaaaaaaaa", password))
        self.assertUsernameFormatError(controller.signup("a4t%", password))
        self.assertPasswordFormatError(controller.signup(username, ''))
        self.assertPasswordFormatError(controller.signup(username, "aaaaaaaaaaaaaaaaaaaaa"))
        self.assertPasswordFormatError(controller.signup(username, "a4t%"))

    def testLoginExceptions(self):
        controller = Controller()

        self.assertInvalidCredentials(controller.login("cam",'password'))

    def testAddChatroomGetMessagesByIndex(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'

        id = self.getID(controller.signup(username, password))

        controller.create(id,password,chatroom)

        for i in xrange(10):
            self.assertOk(controller.send(id,password,chatroom,"message" + str(i)))

        response = controller.get(id, password, chatroom, 4)

        messages = self.getMessages(response)

        for i in xrange(5,10):
            message = messages[i-5]
            self.assertEquals(message['username'], username)
            self.assertEquals(message['text'], 'message' + str(i))

        self.assertLastUpdate(response, 9)

    def testGetMessagesExceptions(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        controller.create(id, password, chatroom)

        self.assertChatroomDoesNotExist(controller.get(id,password, chatroom +'2',-1))
        self.assertInvalidCredentials(controller.get(id,password +'2', chatroom, -1))

        controller.block(id,password,chatroom,username2)
        self.assertUserBanned(controller.get(id2,password,chatroom,-1))

    def testGetMessagesByTime(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        controller.create(id, password, chatroom)

        for i in xrange(10):
            controller.send(id,password,chatroom, 'message' + str(i))

        time.sleep(61)
        for i in xrange(10, 20):
            controller.send(id, password, chatroom, 'message' + str(i))

        response = controller.get(id,password,chatroom,None)

        messages = self.getMessages(response)

        for i in xrange(10,20):
            message = messages[i-10]
            self.assertEquals(message['username'], username)
            self.assertEquals(message['text'], 'message' + str(i))

        self.assertLastUpdate(response, 19)

    def testAddChatroomExceptions(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'

        id = self.getID(controller.signup(username, password))

        controller.create(id, password, chatroom)
        self.assertDuplicateChatroom(controller.create(id,password,chatroom))
        self.assertChatroomFormatError(controller.create(id,password,""))
        self.assertChatroomFormatError(controller.create(id, password, "aaaaaaaaaaaaaaaaaaaaa"))
        self.assertChatroomFormatError(controller.create(id, password, "a4t%"))
        self.assertInvalidCredentials(controller.create(id + 1, password, chatroom + "2"))
        self.assertInvalidCredentials(controller.create(id, password + "2", chatroom + "3"))

    def testSetAlias(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        newUsername = 'cam2'

        id = self.getID(controller.signup(username, password))

        self.assertOk(controller.set_alias(id,password,newUsername))

        id2 = self.getID(controller.login(newUsername,password))

        self.assertEqual(id, id2)



    def testSetAliasExceptions(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'
        newUsername = 'cam3'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        self.assertDuplicateUsername(controller.set_alias(id,password,username2))
        self.assertInvalidCredentials(controller.set_alias(id,password+'2', newUsername))

    def testJoin(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'

        id = self.getID(controller.signup(username, password))

        controller.create(id,password,chatroom)

        self.assertOk(controller.join(id, password, chatroom))

    def testJoinExceptionsAndBlock(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        controller.create(id,password,chatroom)

        self.assertChatroomDoesNotExist(controller.join(id,password,chatroom+'2'))
        self.assertInvalidCredentials(controller.join(id,password+'2', chatroom))

        controller.block(id,password,chatroom,username2)

        self.assertUserBanned(controller.join(id2,password,chatroom))

    def testDelete(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        controller.create(id, password, chatroom)

        self.assertOk(controller.join(id2, password, chatroom))

        self.assertOk(controller.delete(id,password,chatroom))

        self.assertChatroomDoesNotExist(controller.join(id2,password,chatroom))

    def testDeleteExceptions(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        controller.create(id, password, chatroom)

        self.assertNotOwner(controller.delete(id2,password,chatroom))
        self.assertInvalidCredentials(controller.delete(id,password + '2', chatroom))
        self.assertChatroomDoesNotExist(controller.delete(id,password,chatroom + '2'))

    def testBlockExceptions(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        controller.create(id, password, chatroom)

        self.assertUserNotFound(controller.block(id,password, chatroom,username2+'2'))
        self.assertInvalidCredentials(controller.block(id, password+'2', chatroom, username2))
        self.assertNotOwner(controller.block(id2,password, chatroom, username2))
        self.assertUserIsOwner(controller.block(id,password,chatroom,username))
        self.assertChatroomDoesNotExist(controller.block(id,password,chatroom+'2', username2))

    def testUnblock(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        controller.create(id, password, chatroom)

        controller.block(id, password, chatroom, username2)

        self.assertOk(controller.unblock(id, password, chatroom, username2))

        self.assertOk(controller.join(id2,password, chatroom))

    def testUnblockExceptions(self):
        controller = Controller()
        username = 'cam'
        password = 'password'
        chatroom = 'camsPlace'
        username2 = 'cam2'

        id = self.getID(controller.signup(username, password))
        id2 = self.getID(controller.signup(username2, password))

        controller.create(id, password, chatroom)

        self.assertUserNotFound(controller.unblock(id,password, chatroom,username2+'2'))
        self.assertInvalidCredentials(controller.unblock(id, password+'2', chatroom, username2))
        self.assertNotOwner(controller.unblock(id2,password, chatroom, username2))
        self.assertChatroomDoesNotExist(controller.unblock(id, password, chatroom + '2', username2))
        self.assertUserNotOnList(controller.unblock(id,password,chatroom,username2))

    def getID(self, response):
        responseDict = json.loads(response)
        self.assertEqual(len(responseDict), 2)

        self.assertEqual(responseDict['responseType'], 'Ok')

        id = responseDict['userID']

        self.assertIsInstance(id, int)
        return id

    def assertDuplicateUsername(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'DuplicateUsername')
        self.assertEqual(len(responseDict), 1)

    def assertUsernameFormatError(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'InvalidUsername')
        self.assertEqual(len(responseDict), 1)

    def assertPasswordFormatError(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'InvalidPassword')
        self.assertEqual(len(responseDict), 1)

    def assertInvalidCredentials(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'InvalidCredentials')
        self.assertEqual(len(responseDict), 1)

    def assertOk(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'Ok')
        self.assertEqual(len(responseDict), 1)

    def assertDuplicateChatroom(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'DuplicateChatroom')
        self.assertEqual(len(responseDict), 1)

    def assertChatroomFormatError(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'InvalidChatroom')
        self.assertEqual(len(responseDict), 1)

    def getMessages(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'Ok')
        self.assertEqual(len(responseDict), 3)

        return responseDict['messages']

    def assertLastUpdate(self, response, lastUpdate):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'Ok')
        self.assertEqual(len(responseDict), 3)

        self.assertEqual(responseDict['lastUpdate'], lastUpdate)

    def assertChatroomDoesNotExist(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'ChatroomDoesNotExist')
        self.assertEqual(len(responseDict), 1)

    def assertUserBanned(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'Blocked')
        self.assertEqual(len(responseDict), 1)

    def assertNotOwner(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'NotOwner')
        self.assertEqual(len(responseDict), 1)

    def assertUserNotFound(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'UserDoesNotExist')
        self.assertEqual(len(responseDict), 1)

    def assertUserIsOwner(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'UserIsOwner')
        self.assertEqual(len(responseDict), 1)

    def assertUserNotOnList(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'UserNotOnList')
        self.assertEqual(len(responseDict), 1)


unittest.main()