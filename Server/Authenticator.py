#!/usr/bin/python

from log_in import dbHandler 

class Authenticator:
    def __init__(self):

        self.db = dbHandler("d8949uhaqoqd28","gmultvozsunwxb",
        "6b0f18a546857583252b8da92d3dfcbc811de51fc3ace445b3f972e35aba2f7f",
        "ec2-54-225-236-102.compute-1.amazonaws.com",5432)

    def authenticateByID(self, userID, pw):

        user= self.db.findByID(userID)

        if user != None:
            if pw ==user.password :
                return True
            else:
                return False 
        else:
            return False
      
    

    def authenticateByName(self,username,pw):
        user= self.db.findByName(username)

        if user !=None:
            if pw == user.password:
                return True
            else: 
                return False
        else:
            return False 

