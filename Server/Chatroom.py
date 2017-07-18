# Created by Cam Southcott

class Chatroom:

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.bannedUsers = {}
        self.messages = []

    # Adds a message to the chatroom
    # Input:
    #   message : Message : Not None
    # Returns:
    #   nothing
    # Exceptions:
    #   UserBannedException
    def addMessage(self, message):
        self.__assertUnbanned(message.user)
        self.messages.append(message)

    # get all messages after and including the specifed time
    # Input:
    #   time : Int : Not None
    #   user : User : Not None
    # Returns:
    #   ( idOfLastMessage : Int, [Message])
    # Exceptions:
    #   UserBannedException
    def getMessagesByTime(self, time, user):
        self.__assertUnbanned(user)
        if len(self.messages) <= 0:
            return (-1, [])
        index = self.__binarySearch(time, 0, len(self.messages) - 1)

        if index < 0:
            return (len(self.messages) - 1, self.messages)
        elif index >= len(self.messages):
            return (len(self.messages) - 1, [])
        else:
            return (len(self.messages) - 1, self.messages[index:])

    # binary search method for finding all messages that occur after and including the time specified
    # Input:
    #   time : Int : Not None
    #   start : Int : Not None
    #   end : Int : Not None
    # Returns:
    #   the first index with a message that has time >= to the time : Int
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

    # returns all messages with index > start
    # Input:
    #   start : Int : Not None
    #   user : User : Not None
    # Returns:
    #   [Message]
    # Exceptions:
    #   NotOwnerException
    def getMessagesByIndex(self, start, user):
        self.__assertUnbanned(user)
        if start < 0:
            return self.messages
        elif len(self.messages) < 1 or start >= len(self.messages):
            return []
        else:
            return self.messages[start+1:]

    # bans user from the chatroom
    # Input:
    #   owner : User : Not None
    #   user : User : Not None
    # Returns:
    #   nothing
    # Exceptions:
    #   NotOwnerException
    #   UserIsOwnerException
    def banUser(self, owner, user):
        self.__assertOwner(owner)

        if owner.id == user.id:
            raise UserIsOwnerException

        self.__banUser(user)

    # unbans user from the chatroom
    # Input:
    #   owner : User : Not None
    #   user : User : Not None
    # Returns:
    #   nothing
    # Exceptions:
    #   NotOwnerException
    #   UserNotBannedException
    def unbanUser(self, owner, user):
        self.__assertOwner(owner)

        if not self.__userIsBanned(user):
            raise UserNotBannedException

        self.__unbanUser(user)

    # Checks if user is banned from the chatroom
    # Input:
    #   user : User : Not None
    # Returns:
    #   bool
    def __userIsBanned(self, user):
        try:
            return self.bannedUsers[user.id]
        except KeyError:
            return False

    # Bans user from the chatroom
    # Input:
    #   userID : User : Not None
    # Returns:
    #   nothing
    def __banUser(self, user):
        self.bannedUsers[user.id] = True

    # unbans user from chatroom
    # Input:
    #   userID : User : Not None
    # Returns:
    #   nothing
    def __unbanUser(self, user):
        try:
            self.bannedUsers.pop(user.id)
        except KeyError:
            pass

    # Makes sure the user attampting a method that requires owner permissions is the owner of this chatroom
    # Input:
    #   owner : User : Not None
    # Returns:
    #   nothing
    # Exceptions:
    #   NotOwnerException
    def __assertOwner(self, owner):
        if self.owner is None or owner.id != self.owner.id:
            raise NotOwnerException

    # Makes sure the user attempting a method on this chatroom is not banned
    # Input:
    #   userID : User : Not None
    # Returns:
    #   nothing
    # Exceptions:
    #   UserBannedException
    def __assertUnbanned(self, user):
        if self.__userIsBanned(user):
            raise UserBannedException

class NotOwnerException:
    pass

class UserBannedException:
    pass

class UserNotBannedException:
    pass

class UserIsOwnerException:
    pass