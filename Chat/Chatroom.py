# Created by Cam Southcott

class Chatroom:

    def __int__(self, name, owner):
        self.name = name
        self.owner = owner
        self.bannedUsers = {}
        self.messages = []

    def addMessage(self, owner, message):
        self.__assertOwner(owner)
        self.__assertUnbanned(message.userID)

    def banUser(self, owner, userID):
        self.__assertOwner(owner)
        self.__banUser(userID)

    def unbanUser(self, owner, userID):
        self.__assertOwner(owner)

        if not self.__userIsBanned(userID):
            raise UserNotBannedException

        self.__unbanUser(userID)

    def __userIsBanned(self, userID):
        try:
            return self.bannedUsers[userID]
        except KeyError:
            return false

    def __banUser(self, userID):
        self.bannedUsers[userID] = true

    def __unbanUser(self, userID):
        try:
            self.bannedUsers.pop(userID)
        except KeyError:
            pass

    def __assertOwner(self, owner):
        if owner != self.owner:
            raise NotOwnerException

    def __assertUnbanned(self, userID):
        if self.__userIsBanned(userID):
            raise UserBannedException

class NotOwnerException:
    pass

class UserBannedException:
    pass

class UserNotBannedException:
    pass