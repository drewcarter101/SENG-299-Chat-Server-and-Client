import unittest
from ChatSystem import *
import time

class ChatSystemTest (unittest.TestCase):
    def testInit(self):
        chatSystem = ChatSystem()

        self.assertEqual(len(chatSystem.chatrooms), 1)

    def testSignupAndLogin(self):
        chatSystem = ChatSystem()
        username = "aaaaaaaaaaaaaaaaaaaa"
        password = 'password'
        userID1 = chatSystem.signup(username, password)
        userID2 = chatSystem.login(username, password)

        self.assertIsInstance(userID2, int)
        self.assertEqual(userID1, userID2)

    def testSignupUsernameBadCharacter(self):
        chatSystem = ChatSystem()
        username = "cam$"
        password = 'password'

        try:
            chatSystem.signup(username, password)
            self.fail()
        except UsernameFormatException:
            pass

    def testSignupUsernameTooLong(self):
        chatSystem = ChatSystem()
        username = "aaaaaaaaaaaaaaaaaaaaa"
        password = 'password'

        try:
            chatSystem.signup(username, password)
            self.fail()
        except UsernameFormatException:
            pass

    def testSignupUsernameBlank(self):
        chatSystem = ChatSystem()
        username = ""
        password = 'password'

        try:
            chatSystem.signup(username, password)
            self.fail()
        except UsernameFormatException:
            pass

    def testSignupPasswordBadCharacter(self):
        chatSystem = ChatSystem()
        username = "cam"
        password = 'passw#ord'

        try:
            chatSystem.signup(username, password)
            self.fail()
        except PasswordFormatException:
            pass

    def testSignupPasswordTooLong(self):
        chatSystem = ChatSystem()
        username = "cam"
        password = "aaaaaaaaaaaaaaaaaaaaa"

        try:
            chatSystem.signup(username, password)
            self.fail()
        except PasswordFormatException:
            pass

    def testSignupPasswordBlank(self):
        chatSystem = ChatSystem()
        username = "cam"
        password = ""

        try:
            chatSystem.signup(username, password)
            self.fail()
        except PasswordFormatException:
            pass

    def testSignupDuplicate(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatSystem.signup(username, password)

        try:
            chatSystem.signup(username, password)
            self.fail()
        except DuplicateUsernameException:
            pass

    def testLoginNotFound(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'

        try:
            chatSystem.login(username, password)
            self.fail()
        except DuplicateUsernameException:
            pass

    def testAddChatroom(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(userID, chatroomName)

        self.assertEqual(len(chatSystem.chatrooms), 2)
        self.assertIsNone(chatSystem.chatrooms[chatroomName])

    def testAddChatroomDuplicate(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(userID, chatroomName)

        try:
            chatSystem.addChatroom(userID, chatroomName)
            self.fail()
        except DuplicateChatroomException:
            pass

    def testAddChatroomRoomNameBlank(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = ''

        userID = chatSystem.signup(username, password)

        try:
            chatSystem.addChatroom(userID, chatroomName)
            self.fail()
        except ChatroomFormatException:
            pass

    def testAddChatroomRoomNameTooLong(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = "aaaaaaaaaaaaaaaaaaaaa"

        userID = chatSystem.signup(username, password)

        try:
            chatSystem.addChatroom(userID, chatroomName)
            self.fail()
        except ChatroomFormatException:
            pass

    def testAddChatroomUserNotFound(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        userID = chatSystem.signup(username, password)

        try:
            chatSystem.addChatroom(userID + 1, chatroomName)
            self.fail()
        except UserNotFoundException:
            pass

    def testJoinChatroom(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        userID = chatSystem.signup(username, password)
        chatSystem.addChatroom(userID, chatroomName)

        chatSystem.joinChatroom(chatroomName, userID)

    def testJoinChatroomDoesNotExist(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        userID = chatSystem.signup(username, password)

        try:
            chatSystem.joinChatroom(chatroomName, userID)
            self.fail()
        except ChatroomDoesNotExistException:
            pass

    def testJoinChatroomUserNotFound(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        userID = chatSystem.signup(username, password)

        try:
            chatSystem.joinChatroom(chatroomName, userID + 1)
            self.fail()
        except UserNotFoundException:
            pass

    def testJoinChatroomUserBanned(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)
        chatSystem.banUser(ownerID, chatroomName, username)

        try:
            chatSystem.joinChatroom(chatroomName, userID + 1)
            self.fail()
        except UserBannedException:
            pass

    def testBanUser(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)
        chatSystem.banUser(ownerID, chatroomName, username)

        self.assertEqual(len(chatSystem.chatrooms[chatroomName].bannedUsers), 1)

    def testBanUserNotFound(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)

        try:
            chatSystem.banUser(ownerID, chatroomName, username + '123')
            self.fail()
        except UserNotFoundException:
            pass

    def testBanUserNotOwner(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)

        try:
            chatSystem.banUser(userID, chatroomName, ownername)
            self.fail()
        except NotOwnerException:
            pass

unittest.main()