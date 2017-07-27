


class DBHandler:

    def close(self):
        pass

    def insert(self, username, password):
        pass

    def findByID(self, user_id):
        pass

    def findByName(self, username):
        pass

    def updateUser(self, user_id, new_username, new_password):
        pass

class DuplicateNameException(Exception):
    pass

class IDNotExistException(Exception):
    pass

class DBException(Exception):
    pass


from DBHandlerInMem import DBHandlerInMem

dbHandler = DBHandlerInMem()