# Created by Cam Southcott

class Chatroom:

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.bannedUsers = {}
        self.messages = []

    def addMessage(self, message):
        self.__assertUnbanned(message.userID)
        self.messages.append(message)

    def getMessagesByTime(self, time, userID):
        self.__assertUnbanned(userID)
        if len(self.messages) <= 0:
            return (-1, [])
        index = self.__binarySearch(time, 0, len(self.messages) - 1)

        if index < 0:
            return (len(self.messages) - 1, self.messages)
        elif index >= len(self.messages):
            return (len(self.messages) - 1, [])
        else:
            return (len(self.messages) - 1, self.messages[index:])

    #binary search method for finding all messages that occur after and including the time specified
    #returns the first index with a message that has time >= to the time
    def __binarySearch(self,time, start, end):
        if start > end:
            return start

        mid = (start + end) // 2

        diff = self.messages[mid].time - time

        if diff > 0:
            return self.__binarySearch(time, start, mid - 1)
        elif diff == 0:
            return start
        else:
            return self.__binarySearch(time, mid + 1, end)

    def getMessagesByIndex(self, start, userID):
        self.__assertUnbanned(userID)
        if start < 0:
            return self.messages
        elif len(self.messages) < 1 or start >= len(self.messages):
            return []
        else:
            return self.messages[start+1:]

    def banUser(self, owner, userID):
        self.__assertOwner(owner)

        if owner == userID:
            raise UserIsOwnerException

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
            return False

    def __banUser(self, userID):
        self.bannedUsers[userID] = True

    def __unbanUser(self, userID):
        try:
            self.bannedUsers.pop(userID)
        except KeyError:
            pass

    #Makes sure the user attampting a method that requires owner permissions is the owner of this chatroom
    def __assertOwner(self, owner):
        if owner != self.owner:
            raise NotOwnerException

    #Makes sure the user attempting a method on this chatroom is not banned
    def __assertUnbanned(self, userID):
        if self.__userIsBanned(userID):
            raise UserBannedException

class NotOwnerException:
    pass

class UserBannedException:
    pass

class UserNotBannedException:
    pass

class UserIsOwnerException:
    pass