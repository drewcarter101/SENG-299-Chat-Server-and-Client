#!/usr/bin/env python

import sys
import os
import re
import json
from InputHandler import InputHandler as InputHandler
import Credentials as cred
import ClientStateInfo as csi

class Chat():

    def __init__(self):
        self.ClientUsername=""

        self.messages={}
        self.notTryingSignUp=True

        self.credential_errors={"InvalidUsername": "Usernames are alphanumeric and cannot be blank", "InvalidPassword": "Passwords are alphanumeric and cannot be blank", "Invalid_pairing": "Either the password or username entered is incorrect", "DuplicateUsername": "This user name already exists, please enter a valid username"}#fill in later
        
        #Help text
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
            self.helpText=myfile.read()
            

    def sign_up(self, username,password):
        #placeholder for method in serverwrapper
        return "Ok"

    def login(self, username,password):
        #placeholder for method in serverwrapper
        return "Ok"

    def set_alias(self, username, password, newUsername):
        #if bad
        ##return credential_Error[error message]
        #if successful change clientusername to newusername
        return "Name succesfully changed!\n"

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
            if self.login(tempUser, tempPass)== "Ok" and self.notTryingSignUp:
                self.ClientUsername=tempUser
                print "Login complete!"
                break
            elif self.login(tempUser, tempPass) == "InvalidCredentials":
                if self.notTryingSignUp: print self.credential_errors["Invalid_pairing"]
                response= raw_input("Press 's' to sign up as a new user or press any key to retry login\n")
                if response== 's':
                    self.notTryingSignUp=False
                    print "Beginnng sign up process..."
                    if self.sign_up(tempUser, tempPass)=="Ok":
                        self.ClientUsername=tempUser
                        print "Sign up complete, you are now logged in"
                        break
                    else:
                        print self.credential_errors[sign_up(tempUser, tempPass)]
                elif response=="/quit":
                    self.quit()
                elif response=="/help":
                    print self.helpText
            else: 
                print "Invalid entry"

        #Main Program loop
        print "\nWhat do you want to do now?"
        while True: 
            input_list= raw_input(">> ")
            parser=InputHandler(input_list.split(" "), cred.getCredentials(), csi.getCurrentChatroom(), self.ClientUsername)
            output= json.loads(parser.to_json())
            if output["Type"]=="client_command":
                self.peformAction(output["requestType"], output["value"])
            elif output["Type"]=="error":
                print output["value"]
            else:
                #else send output to server to decide what to do next
                #server_Send(output)
                #result=json.loads(server.recieve())
                #if result["requestType"]=="normal":
                    #add result["message"] to list of self.messages:
                    #self.messages[result["message"] ]="unseen"
                #else:
                    #print errors[result["message"]]
                print(output["value"])
            #result=json.loads(server.recieve())
            #if result["requestType"]=="normal":
                #add result["message"] to list of self.messages:
                #self.messages[result["message"] ]="unseen"
            #for key, value in self.messages.iteritems() :
                #if value=="unseen":
                    #print key
                    #value="seen"

    def quit(self):
        sys.exit()

if __name__ == "__main__":
    chat = Chat()
    chat.run() 
