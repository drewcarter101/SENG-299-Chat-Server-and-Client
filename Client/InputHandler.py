# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import re
import json
from ServerWrapper import ServerWrapper as ServerWrapper
import ClientStateInfo as csi
import Credentials as cred
from colorama import init
from colorama import Fore, Back, Style
init()

class InputHandler():


    def send_command(self, commands, user_data, chatroom):
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

            if data["requestType"] == "join":
                data["response"] == self.wrapper.join(user_data["userID"],user_data["password"],chatroom)["responseType"]
                if data["response"] == "Ok":
                    csi.setCurrentChatroom(chatroom)

            elif data["requestType"] == "create":
                data["response"] == self.wrapper.create(user_data["userID"],user_data["password"],chatroom)["responseType"]
                if data["response"] == "Ok":
                    csi.setCurrentChatroom(chatroom)
                    
            elif data["requestType"] == "block":
                data["response"] == self.wrapper.block(user_data["userID"],user_data["password"],data["value"] ,chatroom)["responseType"]

            elif data["requestType"] == "unblock":
                data["response"] == self.wrapper.unblock(user_data["userID"],user_data["password"],data["value"] ,chatroom)["responseType"]

            elif data["requestType"] == "delete":
                data["response"] == self.wrapper.delete(user_data["userID"],user_data["password"],chatroom)["responseType"]
                if data["response"] == "Ok":
                    csi.setCurrentChatroom("general")
        return data

    def send_message(self, message, input_list, errors, user_data, chatroom):
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
            data["response"] == self.wrapper.send(user_data["userID"],user_data["password"],chatroom, data["value"])["responseType"]
        return data
		

    def parser(self, input_list, user_data, chatroom):
        self.wrapper=ServerWrapper()
        self.chatroom_commands =["join","create","block", "unblock", "delete","set_alias", "help", "quit"]
        #linux shell: formats={":b": '\033[1m', "b:": '\033[0m',":u": '\033[4m', "u:": '\033[0m', ":h": '\033[91m', "h:": '\033[0m', ":happy:": u'\U0001f604', ":sad:": u'\U0001F622', ":angry:": u'\U0001F620', ":bored:": u'\U0001F634', ":thumbsup:": u'\U0001F44D', ":thumbsdown:": u'\U0001F44E', ":highfive:": u'\U0000270B'}
        formats={":b": '\033[1m', "b:": '\033[22m ',":u": '__', "u:": '__', ":h": '\033[31m \033[1m', "h:": '\033[22m \033[39m ', ":happy:": ":)", ":sad:": ":(", ":angry:": ">:-(", ":bored:": "(-_-)" , ":thumbsup:": "(^ ^)b", ":thumbsdown:": "(- -)p", ":highfive:": "^_^/"}
        errors={"invalid_command" :"'{}' does not exist, Type /help for a list of chat commands", "invalid_useOf_command" :"Invalid arguments for '{}', Type /help for a list of chat commands"}
        input=" ".join([formats.get(item, item) for item in input_list])

        pattern1="^/(?:({})) ([A-Za-z0-9_]+)$".format("|".join(self.chatroom_commands))
        pattern2="^/(?:({}))$".format("|".join(self.chatroom_commands[6:])) 
        general_pattern="(?:{}|{})".format(pattern1, pattern2) 
        #highlight_Pattern=":h (.*?) h:"
		

        command_input=re.search(general_pattern, input)

        
        if command_input is not None:
            self.output=self.send_command([command_input.group(1), command_input.group(2), command_input.group(3)], user_data, chatroom)
        else:
            self.output= self.send_message(input, input_list, errors, user_data, chatroom)
			
        return self.output
			
    def __init__(self, serverWrapper, clientStateInfo):
        self.wrapper=serverWrapper()
        self.csi=clientStateInfo()
		self.cred=self.csi.credentials
		
        self.credential_errors={"Ok": "Success","InvalidUsername": "Usernames are alphanumeric and cannot be blank", "InvalidPassword": "Passwords are alphanumeric and cannot be blank", "Invalid_pairing": "Either the password or username entered is incorrect", "DuplicateUsername": "This user name already exists, please enter a valid username", "ParametersMissing" : "ParametersMissing"}
        self.system_errors={"Ok": "Success","InvalidCredentials": "Your user credentials are invalid", "ParametersMissing" : "ParametersMissing", "Blocked": "You have been blocked from this chatroom", "ChatroomDoesNotExist": "Sorry, this chatroom does not exist", "InvalidMessage": "Your missage is invalid", "DuplicateChatroom": "This chatroom already exists", "UserDoesNotExist": "This User does not exist", "NotOwner": "You are not the owner of this chatroom, only owners can perform this operation", "UserNotOnList": "This user was never blocked"}
        #Help text
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
            self.helpText=myfile.read()
        self.run()

    def set_alias(self, userid, password, newUsername):
        tempResponse= self.wrapper.set_alias(userid,password,newUsername)["responseType"]
        return self.credential_errors[tempResponse]
        

    def peformAction(self, command, value):
        if command=="set_alias":
            print self.set_alias(self.cred.userID, self.cred.password, value)
        elif command== "help":
            print self.helpText
        elif command =="quit":
            self.quit()
        return

    def run(self):

        #Main Program loop
        print "\nWhat do you want to do now?"
        while True: 
            input_list= raw_input(">> ")
			credObj={"userID": self.cred.userID, "password": self.cred.password}
            output=self.parser(input_list.split(" "), credObj, self.csi.chatroom)
            if output["Type"]=="client_command":
                self.peformAction(output["requestType"], output["value"])
            elif output["Type"]=="error":
                print output["value"]
            else:
			   print self.system_errors[output["response"]]
            
    def quit(self):
        sys.exit()
	
