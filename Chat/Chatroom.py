# Created by Cam Southcott

import time

class Chatroom:

    def __int__(self, name, owner):
        self.name = name
        self.owner = owner
        self.bannedUsers = {}
        self.messages = []

    def addMessage(self, message):
        self.__assertUnbanned(message.userID)
        messages.append(message)

    def getMessagesByTime(self, time):
        self.__assertUnbanned(message.userID)
        if len(message) <= 0:
            return []
        index = self.__binarySearch(time, 0, len(messages) - 1) + 1

        if index < 0:
            return (len(messages) - 1, messages)
        elif index >= len(messages):
            return (len(messages) - 1, [])
        else:
            return (len(messages) - 1, messages[index:])

    #binary search method for finding all messages that occur after and including the time specified
    #returns the first index with a message that has time >= to the time
    def __binarySearch(self,time, start, end):
        if start > end:
            return start

        mid = (start + end) // 2

        diff = messages[mid].time - time

        if diff < 0:
            return self.__binarySearch(time, start, mid - 1)
        elif dif == 0:
            return start
        else:
            return self.__binarySearch(time, mid + 1, end)

    def getMessagesByIndex(self, start):
        self.__assertUnbanned(message.userID)
        if start < 0:
            return messages
        elif len(message < 1):
            return []
        else:
            return messages[start+1:]

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