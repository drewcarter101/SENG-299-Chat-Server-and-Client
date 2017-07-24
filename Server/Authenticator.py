#!/usr/bin/python

from DBHandler import dbHandler

class Authenticator:
    def __init__(self):

        self.db = dbHandler

    def authenticateByID(self, userID, pw):

        user= self.db.findByID(userID)

        if user is None:
            return False
        else:
            if pw == user.password:
                return True
            else:
                return False 

        
      
    

    def authenticateByName(self,username,pw):
        user= self.db.findByName(username)

        if user:
            if pw == user.password:
                return True
            else: 
                return False
        else:
            return False 

