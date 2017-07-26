#!/usr/bin/env python

import sys
import os
import re
import json
from InputHandler import InputHandler as InputHandler
import Credentials as cred
import ClientStateInfo as csi
from ServerWrapper import ServerWrapper as ServerWrapper
from MessageUpdater import MessageUpdater as MessageUpdater

class Chat():

    def __init__(self):
        self.ClientUsername
        self.wrapper=ServerWrapper()
        self.notTryingSignUp=True

        self.credential_errors={"InvalidUsername": "Usernames are alphanumeric and cannot be blank", "InvalidPassword": "Passwords are alphanumeric and cannot be blank", "Invalid_pairing": "Either the password or username entered is incorrect", "DuplicateUsername": "This user name already exists, please enter a valid username", "ParametersMissing" : "ParametersMissing"}
        self.system_errors{"InvalidCredentials": "Your user credentials are invalid", "ParametersMissing" : "ParametersMissing", "Blocked": "You have been blocked from this chatroom", "ChatroomDoesNotExist": "Sorry, this chatroom does not exist", "InvalidMessage": "Your missage is invalid", "DuplicateChatroom": "This chatroom already exists", "UserDoesNotExist": "This User does not exist", "NotOwner": "You are not the owner of this chatroom, only owners can perform this operation", "UserNotOnList": "This user was never blocked"}
        #Help text
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
            self.helpText=myfile.read()

    def set_alias(self, userid, password, newUsername):
        tempResponse= self.wrapper.set_alias(userid,password,newUsername)["responseType"]:
        if tempResponse == "Ok":
            self.ClientUsername = newUsername
            return "Name succesfully changed!\n"
        else:
            return self.credential_errors[tempResponse]
        

    def peformAction(self, command, value):
        if command=="set_alias":
            print self.set_alias(cred.getCredentials()["userID"], cred.getCredentials()["password"], value)
        elif command== "help":
            print self.helpText
        elif command =="quit":
            self.quit()
        return

    def run(self):
        
        print "Welcome! Type '/quit' to exit or '/help' for assistance."
        print "Login/sign-up below:\n"
        #login/signup screen
        while True:
            tempUser=raw_input("Please enter a username: " + self.credential_errors["InvalidUsername"]+ "\n")
            if tempUser=="/quit":
                self.quit()
            elif tempUser=="/help":
                print self.helpText
            tempPass=raw_input("Please enter your password, if your account does not exist, you will be prompted to sign up: " + self.credential_errors["InvalidPassword"]+ "\n")
            if tempPass=="/quit":
                self.quit()
            elif tempPass=="/help":
                print self.helpText
            if self.wrapper.login(tempUser, tempPass)== "Ok" and self.notTryingSignUp:
                self.ClientUsername=tempUser
                print "Login complete!"
                break
            elif self.wrapper.login(tempUser, tempPass) == "InvalidCredentials":
                if self.notTryingSignUp: print self.credential_errors["Invalid_pairing"]
                response= raw_input("Press 's' to sign up as a new user or press any key to retry login\n")
                if response== 's':
                    self.notTryingSignUp=False
                    print "Beginnng sign up process..."
                    if self.wrapper.signup(tempUser, tempPass)=="Ok":
                        self.ClientUsername=tempUser
                        print "Sign up complete, you are now logged in"
                        break
                    else:
                        print self.credential_errors[self.wrapper.signup(tempUser, tempPass)]
                elif response=="/quit":
                    self.quit()
                elif response=="/help":
                    print self.helpText
            else: 
                print "Invalid entry"

        #Main Program loop
        self.lastUpdate=None
        print "\nWhat do you want to do now?"
        while True: 
            input_list= raw_input(">> ")
            parser=InputHandler(input_list.split(" "), cred.getCredentials(), csi.getCurrentChatroom(), self.ClientUsername)
            output= parser.to_dict()
            if output["Type"]=="client_command":
                self.peformAction(output["requestType"], output["value"])
            elif output["Type"]=="error":
                print output["value"]
            else: 
                if output["response"] == "Ok":
                    print "success"
                else:
                    print self.system_errors[output["response"]]

            self.msgUpdater=MessageUpdater(cred.getCredentials(), csi.getCurrentChatroom(), output, self.lastUpdate)

            if self.msgUpdater["Type"]=="error":
                print self.system_errors[self.msgUpdater["response"]]
            else:
                self.lastUpdate=self.msgUpdater["response"][0]
                for i in self.msgUpdater["response"][1]:
                    print i

    def quit(self):
        sys.exit()

if __name__ == "__main__":
    chat = Chat()
    chat.run() 
