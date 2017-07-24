from DBHandler import *
from User import User


class DBHandlerInMem(DBHandler):
    def __init__(self):
        self.usersByName = {}
        self.usersByID = {}
        self.nextID = 0

    def close(self):
        pass

    def findByID(self, user_id):
        try:
            return self.usersByID[user_id]
        except KeyError:
            return None

    def findByName(self, username):
        try:
            return self.usersByName[username]
        except KeyError:
            return None

    def insert(self, username, password):
        if self.findByName(username):
            raise DuplicateNameException

        id = self.nextID
        self.nextID += 1

        user = User(username,id,password)
        self.usersByID[id] = user
        self.usersByName[username] = user

        return id

    def updateUser(self, user_id, new_username, new_password):
        if self.findByName(new_username):
            raise DuplicateNameException

        user = self.findByID(user_id)

        if user is None:
            raise IDNotExistException

        oldUsername = user.name
        user.name = new_username
        user.password = new_password

        self.usersByName.pop(oldUsername)

        self.usersByName[new_username] = user
