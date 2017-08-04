# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import re
import json
import threading
import time
import os
from Constant import GENERAL_CHATROOM
from ServerWrapper import *
import ClientStateInfo as csi
import Credentials as cred
from colorama import init
from colorama import Fore, Back, Style
init()

class InputHandler():

    ## Handles the parsing, sending and responses of commands
    def send_command(self, commands, user_data, clientStateInfo):
        commands=list(filter(None, commands))
        data = {}

        data["requestType"] = commands[0]
        data["Type"]="normal"

        if len(commands)>1:
            data["value"]=commands[1]
        else:
            data["value"]=None

        if commands[0] == "quit":
            print "Exiting program"
            self.quit()

        else:
            try:
                if data["requestType"] == "join":
        			data["response"] = self.wrapper.join(user_data["userID"],user_data["password"],data["value"])
        			clientStateInfo.chatroom=data["value"]
        			print "Success"
                elif data["requestType"] == "create":
        			data["response"] = self.wrapper.create(user_data["userID"],user_data["password"],data["value"])
        			clientStateInfo.chatroom=data["value"]
        			print "Success"
    
                elif data["requestType"] == "block":
        			data["response"] = self.wrapper.block(user_data["userID"],user_data["password"],data["value"] ,clientStateInfo.chatroom)
        			print "Success"

                elif data["requestType"] == "unblock":
        			data["response"] = self.wrapper.unblock(user_data["userID"],user_data["password"],data["value"] ,clientStateInfo.chatroom)
        			print "Success"
    
                elif data["requestType"] == "delete":
        			data["response"] = self.wrapper.delete(user_data["userID"],user_data["password"],data["value"])
        			clientStateInfo.chatroom=GENERAL_CHATROOM
        			print "Success"

                elif data["requestType"] == "set_alias":
        			data["response"] = self.wrapper.set_alias(user_data["userID"],user_data["password"],data["value"])
        			print "Name succesfully changed"

                elif data["requestType"] == "help":
        			print self.helpText
        			
            except blockedException:
                print "You have been blocked from the chatroom"
            
            except parametersMissingException:
                print "Missing parameters"
            
            except invalidCredentialsException:
                print "Your credentials are invalid"
            
            except chatroomDoesNotExistException:
                print "The chatroom does not exist"
            
            except duplicateChatrooomException:
                print "This chatroom already exists"
            
            except userDoesNotExistException:
                print "The user does not exist"
            
            except notOwnerException:
                print "You are not the owner of the chatroom"
            
            except userNotOnListException:
                print "The user is not in the chatroom"
            
            except invalidChatroomException:
                print "The chatroom name entered is invalid"

            except ServerWrapperException:
                print "Error occured while trying to perform operation"

            except duplicateUsernameException:
				print "This user name already exists, please enter a valid username"
                
            except invalidUsernameException:
                print "Usernames are alphanumeric and cannot be blank"
                
            except invalidPasswordException:
				print "Passwords are alphanumeric and cannot be blank"

        return data

    ## Handles the parsing, sending and responses of normal messages
    def send_message(self, message, input_list, errors, user_data, clientStateInfo):
        data = {}

        if message[0]=="/":
            data["Type"]="error"
            if input_list[0][1:] in self.chatroom_commands:
                data["value"] = errors["invalid_useOf_command"].format(input_list[0])
            else:
                data["value"] = errors["invalid_command"].format(input_list[0])
        else:
			data["Type"]="normal"
			data["value"] = message + "\033[22m \033[39m"
			try:
				data["response"] = self.wrapper.send(user_data["userID"],user_data["password"],clientStateInfo.chatroom, data["value"])
			
			except invalidMessageException:
			    print "The message entered is invalid"
		    
			except blockedException:
				print "You have been blocked from the chatroom"
				
			except parametersMissingException:
				print "Missing parameters"
            
			except invalidCredentialsException:
				print "Your credentials are invalid"
				
			except chatroomDoesNotExistException:
				print "The chatroom does not exist"
				
			except ServerWrapperException:
			    print "Error occured while trying to perform operation"
            
	return data


    ## takes in user input, performs formatting and determines if input is a command or message
    ## and performs the appropriate parsing
    def parser(self, input_list, user_data, clientStateInfo):
        self.output={"Type": "error", "value":""}
        if input_list[0] != "":
            self.chatroom_commands =["join","create","block", "unblock", "delete","set_alias", "help", "quit"]
            formats={":b": '\033[1m', "b:": '\033[22m ',":u": '__', "u:": '__', ":h": '\033[31m \033[1m', "h:": '\033[22m \033[39m ', ":happy:": ":)", ":sad:": ":(", ":angry:": ">:-(", ":bored:": "(-_-)" , ":thumbsup:": "(^ ^)b", ":thumbsdown:": "(- -)p", ":highfive:": "^_^/"}
            errors={"invalid_command" :"'{}' does not exist, Type /help for a list of chat commands", "invalid_useOf_command" :"Invalid arguments for '{}', Type /help for a list of chat commands"}
            input=" ".join([formats.get(item, item) for item in input_list])

            pattern1="^/(?:({})) ([A-Za-z0-9_]+)$".format("|".join(self.chatroom_commands))
            pattern2="^/(?:({}))$".format("|".join(self.chatroom_commands[6:]))
            general_pattern="(?:{}|{})".format(pattern1, pattern2)

            command_input=re.search(general_pattern, input)

            if command_input is not None:
                self.output=self.send_command([command_input.group(1), command_input.group(2), command_input.group(3)], user_data, clientStateInfo)
            else:
                self.output= self.send_message(input, input_list, errors, user_data, clientStateInfo)

        return self.output


    ## constructor initiates variables
    def __init__(self, serverWrapper, clientStateInfo, chat):
		self.wrapper=serverWrapper
		self.csi=clientStateInfo
		self.cred=self.csi.credentials
		self.chat = chat

		#Help text
		__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
			self.helpText=myfile.read()


    # Starts current thread
    def run(self):
		self.stop = False
		self.lastUpdate = None
		self.lastChatroom = self.csi.chatroom
		self.thread = threading.Thread(target=self.__handleInput)
		#allows the program to close regardless of it this thread is running
		self.thread.daemon = True
		self.thread.start()

    # Recieves input from terminal window
    def __handleInput(self):
        print "\nWhat do you want to do now?"
        while True:
            if self.stop:
                return
            input_list= raw_input()[:200]
            credObj={"userID": self.cred.userID, "password": self.cred.password}
            output=self.parser(input_list.split(" "), credObj, self.csi)
            if output["Type"]=="error":
                print output["value"]

    #Stops thread and quits program
    def quit(self):
        self.stop = True
        sys.exit()

