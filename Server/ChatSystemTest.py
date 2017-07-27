import unittest
from ChatSystem import *
from Chatroom import *
import time

class ChatSystemTest (unittest.TestCase):

    def setUp(self):
        dbHandler.usersByName = {}
        dbHandler.usersByID = {}

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
        except UserNotFoundException:
            pass

    def testAddChatroom(self):
        chatSystem = ChatSystem()
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        userID = chatSystem.signup(username, password)

        self.assertIsInstance(userID, int)

        chatSystem.addChatroom(userID, chatroomName)

        self.assertEqual(len(chatSystem.chatrooms), 2)
        chatroom = chatSystem.chatrooms[chatroomName]
        self.assertEqual(userID, chatroom.owner.id)


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

        chatSystem.addChatroom(userID, chatroomName)

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
            chatSystem.joinChatroom(chatroomName, userID)
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

    def testUnbanUser(self):
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

        chatSystem.unbanUser(ownerID, chatroomName, username)

        self.assertEqual(len(chatSystem.chatrooms[chatroomName].bannedUsers), 0)

    def testUnbanUserNotBanned(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)

        self.assertRaises(UserNotBannedException, chatSystem.unbanUser, ownerID, chatroomName, username)

    def testUnbanUserNotOwner(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)

        self.assertRaises(NotOwnerException, chatSystem.unbanUser, userID, chatroomName, ownername)

    def testUnbanUserUserNotFound(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)

        self.assertRaises(UserNotFoundException, chatSystem.unbanUser, ownerID, chatroomName, "cam2")
        self.assertRaises(UserNotFoundException, chatSystem.unbanUser, userID + 10, chatroomName, username)

    def testUnbanUserChatroomNotFound(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        self.assertRaises(ChatroomDoesNotExistException, chatSystem.unbanUser, ownerID, chatroomName, username)

    def testDeleteChatroom(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)
        self.assertEqual(len(chatSystem.chatrooms), 2)

        chatSystem.deleteChatroom(ownerID, chatroomName)
        self.assertEqual(len(chatSystem.chatrooms), 1)

    def testDeleteChatroomExceptions(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)

        self.assertRaises(NotOwnerException, chatSystem.deleteChatroom, userID, chatroomName)
        self.assertRaises(UserNotFoundException, chatSystem.deleteChatroom, userID + 10, chatroomName)
        self.assertRaises(ChatroomDoesNotExistException, chatSystem.deleteChatroom, ownerID, chatroomName + '2')

    def testGetMessagesByIndex(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)

        for i in xrange(10):
            chatSystem.addMessage(chatroomName, ownerID, 'message' + str(i))

        messages = chatSystem.getMessagesByIndex(chatroomName, userID, 0)
        self.assertEqual(messages[0], 9)
        self.assertEqual(len(messages[1]), 9)

        messages = chatSystem.getMessagesByIndex(chatroomName, ownerID, None)
        self.assertEqual(messages[0], 9)
        self.assertEqual(len(messages[1]), 10)

    def testGetMessageByIndexExceptions(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)

        for i in xrange(10):
            chatSystem.addMessage(chatroomName, ownerID, 'message' + str(i))

        self.assertRaises(UserNotFoundException, chatSystem.getMessagesByIndex, chatroomName, userID + 10, -1)
        self.assertRaises(ChatroomDoesNotExistException, chatSystem.getMessagesByIndex, chatroomName + '2', ownerID, -1)

        chatSystem.banUser(ownerID, chatroomName, username)
        self.assertRaises(UserBannedException, chatSystem.getMessagesByIndex, chatroomName, userID, -1)

    def testGetMessageByTimeExceptions(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)
        for i in xrange(10):
            chatSystem.addMessage(chatroomName, ownerID, 'message' + str(i))

        self.assertRaises(UserNotFoundException, chatSystem.getMessagesByTime, chatroomName, userID + 10)
        self.assertRaises(ChatroomDoesNotExistException, chatSystem.getMessagesByTime, chatroomName + '2', ownerID)

        chatSystem.banUser(ownerID, chatroomName, username)
        self.assertRaises(UserBannedException, chatSystem.getMessagesByTime, chatroomName, userID)

    def testSetAlias(self):
        chatSystem = ChatSystem()
        username = 'owner'
        newUsername = 'cam'
        password = 'password'

        userID = chatSystem.signup(username, password)

        chatSystem.set_alias(userID, newUsername, password)

        chatSystem.login(newUsername, password)

    def testSetAliasExceptions(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        self.assertRaises(DuplicateUsernameException, chatSystem.set_alias, ownerID, username, password)
        self.assertRaises(UserNotFoundException, chatSystem.set_alias, userID + 10, username + '2', password)

    def testGetMessageByTime(self):
        chatSystem = ChatSystem()
        ownername = 'owner'
        username = 'cam'
        password = 'password'
        chatroomName = 'camsPlace'

        ownerID = chatSystem.signup(ownername, password)
        userID = chatSystem.signup(username, password)

        chatSystem.addChatroom(ownerID, chatroomName)
        for i in xrange(10):
            chatSystem.addMessage(chatroomName, ownerID, 'message' + str(i))

        time.sleep(61)
        for i in xrange(10, 20):
            chatSystem.addMessage(chatroomName, ownerID, 'message' + str(i))

        messages = chatSystem.getMessagesByTime(chatroomName,ownerID)

        self.assertEqual(messages[0], 19)
        self.assertEquals(len(messages[1]), 10)

unittest.main()