import unittest
import json
from DBHandler import dbHandler
from Controller import Controller


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
        self.assertUsernameFormatError(controller.signup(username, ''))
        self.assertUsernameFormatError(controller.signup(username, "aaaaaaaaaaaaaaaaaaaaa"))
        self.assertUsernameFormatError(controller.signup(username, "a4t%"))

    def testLoginExceptions(self):
        controller = Controller()

        self.assertInvalidCredentials(controller.login("cam",'password'))


    def getID(self, response):
        responseDict = json.loads(response)
        self.assertEqual(len(responseDict), 2)

        self.assertEqual(responseDict['ResponseType'], 'Ok')

        id = responseDict['userID']

        self.assertIsInstance(id, int)
        return id

    def assertDuplicateUsername(self,response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['ResponseType'], 'DuplicateUsername')
        self.assertEqual(len(responseDict), 1)

    def assertUsernameFormatError(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['ResponseType'], 'InvalidUsername')
        self.assertEqual(len(responseDict), 1)

    def assertPasswordFormatError(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['ResponseType'], 'InvalidPassword')
        self.assertEqual(len(responseDict), 1)

    def assertInvalidCredentials(self, response):
        responseDict = json.loads(response)
        self.assertEqual(responseDict['ResponseType'], 'InvalidCredentials')
        self.assertEqual(len(responseDict), 1)


unittest.main()