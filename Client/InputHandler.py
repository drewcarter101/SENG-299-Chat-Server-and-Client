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


    def send_command(self, commands, user_data, clientStateInfo):
        commands=list(filter(None, commands))
        data = {}

        data["requestType"] = commands[0]

        if len(commands)>1:
            data["value"]=commands[1]
        else:
            data["value"]=None

        if commands[0] in self.chatroom_commands[5:]:
            data["Type"]="client_command"
        else:
            data["Type"]="command"

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

        return data

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


    def parser(self, input_list, user_data, clientStateInfo):
        self.chatroom_commands =["join","create","block", "unblock", "delete","set_alias", "help", "quit"]
        #formats={":b": '\033[1m', "b:": '\033[0m',":u": '\033[4m', "u:": '\033[0m', ":h": '\033[91m', "h:": '\033[0m', ":happy:": u'\U0001f604', ":sad:": u'\U0001F622', ":angry:": u'\U0001F620', ":bored:": u'\U0001F634', ":thumbsup:": u'\U0001F44D', ":thumbsdown:": u'\U0001F44E', ":highfive:": u'\U0000270B'}
        formats={":b": '\033[1m', "b:": '\033[22m ',":u": '__', "u:": '__', ":h": '\033[31m \033[1m', "h:": '\033[22m \033[39m ', ":happy:": ":)", ":sad:": ":(", ":angry:": ">:-(", ":bored:": "(-_-)" , ":thumbsup:": "(^ ^)b", ":thumbsdown:": "(- -)p", ":highfive:": "^_^/"}
        errors={"invalid_command" :"'{}' does not exist, Type /help for a list of chat commands", "invalid_useOf_command" :"Invalid arguments for '{}', Type /help for a list of chat commands"}
        input=" ".join([formats.get(item, item) for item in input_list])

        pattern1="^/(?:({})) ([A-Za-z0-9_]+)$".format("|".join(self.chatroom_commands))
        pattern2="^/(?:({}))$".format("|".join(self.chatroom_commands[6:]))
        general_pattern="(?:{}|{})".format(pattern1, pattern2)
        #highlight_Pattern=":h (.*?) h:"


        command_input=re.search(general_pattern, input)


        if command_input is not None:
            self.output=self.send_command([command_input.group(1), command_input.group(2), command_input.group(3)], user_data, clientStateInfo)
        else:
            self.output= self.send_message(input, input_list, errors, user_data, clientStateInfo)

        return self.output


    def __init__(self, serverWrapper, clientStateInfo, chat):
		self.wrapper=serverWrapper
		self.csi=clientStateInfo
		self.cred=self.csi.credentials
		self.chat = chat

		#Help text
		__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
			self.helpText=myfile.read()

    def set_alias(self, userid, password, newUsername):
        try:
            tempResponse= self.wrapper.set_alias(userid,password,newUsername)
            return "Name succesfully changed"
        except (duplicateUsernameException, invalidCredentialsException, parametersMissingException, ServerWrapperException) as exx:
			if type(ex) == duplicateUsernameException:
				print "This user name already exists, please enter a valid username"
			elif type(ex) == invalidUsernameException:
				print "Usernames are alphanumeric and cannot be blank"
			elif type(ex) == invalidPasswordException:
				print "Passwords are alphanumeric and cannot be blank"
			elif type(ex) == ServerWrapperException:
			    print "Error occured while trying to perform operation"
			else:
				print "Parameters are missing"


    def peformAction(self, command, value):
        if command=="set_alias":
            print self.set_alias(self.cred.userID, self.cred.password, value)
        elif command== "help":
            print self.helpText
        elif command =="quit":
            print "Exiting program"
            self.quit()
        return

    def run(self):
		self.stop = False
		self.lastUpdate = None
		self.lastChatroom = self.csi.chatroom
		self.thread = threading.Thread(target=self.__handleInput)
		#allows the program to close regardless of it this thread is running
		self.thread.daemon = True
		self.thread.start()

    def __handleInput(self):
        #Main Program loop
        print "\nWhat do you want to do now?"
        while True:
            if self.stop:
                return
            input_list= raw_input()
            credObj={"userID": self.cred.userID, "password": self.cred.password}
            output=self.parser(input_list.split(" "), credObj, self.csi)
            if output["Type"]=="client_command":
                self.peformAction(output["requestType"], output["value"])
                if self.stop:
                    return
            elif output["Type"]=="error":
                print output["value"]

    def quit(self):
        self.stop = True
        sys.exit()

