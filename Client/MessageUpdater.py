import sys
import os
import re
import json
import ClientStateInfo as csi
import Chat as chat
from ServerWrapper import ServerWrapper as ServerWrapper

class MessageUpdater:
    ServerLocation ='localhost'
    Port= 9321

    def __init__(self, Credentials, Chatroom,LastUpdate=None, Input):
        self.wrapper=ServerWrapper()
        self.userid=Credentials["userID"]
        self.password=Credentials["password"]
        self.chatroom=Chatroom
        self.input=Input

        self.run()
    
    def run(self):
        self.response = self.wrapper.get(self.userid, self.password, self.chatroom)["responseType"]
        if self.response == "Ok"
        

    def blocked(self):
        return

    def chatroomDeleted(self):
        return

