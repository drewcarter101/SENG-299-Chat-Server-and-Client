import unittest
import json
import socket

class ServerTest(unittest.TestCase):

    usernameCount = 0

    def testSignupAndLogin(self):
        username = 'serverTestQ'
        password = 'password'

        id = self.getID(self.getResponse('signup',{'username':username, 'password' : password}))
        loginID = self.getID(self.getResponse('login',{'username':username, 'password' : password}))

    def testChatroom(self):
        username = 'serverTestW'
        username2 = 'serverTestE'
        password = 'password'
        chatroom = 'chatroom2'
        message = 'message'

        id = self.getID(self.getResponse('signup',{'username':username, 'password' : password}))
        id2 = self.getID(self.getResponse('signup', {'username': username2, 'password': password}))

        self.assertOk(self.getResponse('create',{'userID':id, 'password' : password, 'chatroom':chatroom}))
        self.assertOk(self.getResponse('join',{'userID':id, 'password' : password,'chatroom':chatroom}))
        self.assertOk(self.getResponse('send',{'userID':id, 'password' : password,'chatroom':chatroom,'message':message}))

        messages = self.getMessages(self.getResponse('get',{'userID':id, 'password' : password,'chatroom':chatroom}))
        self.assertEquals(len(messages),1)
        self.assertEquals(messages[0]['text'], message)

        self.assertOk(self.getResponse('block',{'userID':id, 'password' : password,'chatroom':chatroom,'userToBlock':username2}))
        self.assertUserBanned(self.getResponse('join',{'userID':id2, 'password' : password,'chatroom':chatroom}))

        self.assertOk(self.getResponse('unblock', {'userID': id, 'password': password, 'chatroom': chatroom,'userToUnblock': username2}))
        self.assertOk(self.getResponse('join',{'userID':id2, 'password' : password,'chatroom':chatroom}))

        self.assertOk(self.getResponse('delete',{'userID':id, 'password' : password,'chatroom':chatroom}))
        self.assertChatroomDoesNotExist(self.getResponse('join',{'userID':id, 'password' : password,'chatroom':chatroom}))

    def testSetAlias(self):
        username = 'serverTestR'
        username2 = 'serverTestT'
        password = 'password'

        id = self.getID(self.getResponse('signup',{'username':username, 'password' : password}))
        id2 = self.getID(self.getResponse('signup', {'username': username2, 'password': password}))

        self.assertDuplicateUsername(self.getResponse('set_alias',{'userID':id, 'password' : password, 'newUsername': username2}))

    def testExceptions(self):
        username ='serverTestY'
        password = 'password'

        self.assertRequestFormatError(self.getResponse('signup',{'username':123, 'password' : password}))
        self.assertRequestFormatError(self.getResponse('asdfqwer',{'username':username, 'password' : password}))
        self.assertParameterMissing(self.getResponse('signup', {'password': password}))


    def assertChatroomDoesNotExist(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'ChatroomDoesNotExist')
        self.assertEqual(len(responseDict), 1)

    def assertRequestFormatError(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'RequestFormatError')
        self.assertEqual(len(responseDict), 1)

    def assertParameterMissing(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'ParametersMissing')
        self.assertEqual(len(responseDict), 1)

    def getResponse(self, requestType, args):
        s = socket.socket()
        requestDict = {'requestType' : requestType}
        requestDict.update(args)
        requestString = json.dumps(requestDict)

        host = socket.gethostname()
        port = 9321

        s.connect((host,port))
        s.send(requestString)

        return s.recv(2048)

    def getMessages(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'Ok')
        self.assertEqual(len(responseDict), 3)

        return responseDict['messages']

    def getID(self, response):
        responseDict = json.loads(response)

        self.assertEqual(responseDict['responseType'], 'Ok')
        self.assertEqual(len(responseDict), 2)

        id = responseDict['userID']

        self.assertIsInstance(id, int)
        return id

    def assertLastUpdate(self, response, lastUpdate):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'Ok')
        self.assertEqual(len(responseDict), 3)

        self.assertEqual(responseDict['lastUpdate'], lastUpdate)

    def assertOk(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'Ok')
        self.assertEqual(len(responseDict), 1)

    def assertUserBanned(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'Blocked')
        self.assertEqual(len(responseDict), 1)

    def assertDuplicateUsername(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['responseType'], 'DuplicateUsername')
        self.assertEqual(len(responseDict), 1)

unittest.main()