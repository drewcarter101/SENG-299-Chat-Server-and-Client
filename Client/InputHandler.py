# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import re
import json
from colorama import init
from colorama import Fore, Back, Style
init()

class InputHandler():


    def send_command(self, commands, user_data, chatroom):
        commands=list(filter(None, commands))
        data = {}
        if commands[0] in self.chatroom_commands[5:]:
            data["Type"]="client_command"
        else:
            data["Type"]="command"
        data["requestType"] = commands[0]
        
        if len(commands)>1: data["value"]=commands[1]
        else: data["value"]=None
        data["userID"] = user_data["userID"]
        data["password"] = user_data["password"]
        data["chatroom"] = chatroom
        json_data = json.dumps(data)
        return json_data

    def send_message(self, message, input_list, errors, user_data, chatroom, username):
        data = {}
        
        if message[0]=="/":
            data["Type"]="error"
            if input_list[0][1:] in self.chatroom_commands:
                data["value"] = errors["invalid_useOf_command"].format(input_list[0])
            else:
                data["value"] = errors["invalid_command"].format(input_list[0])
        else:
            data["Type"]="normal"
            data["requestType"]="message"
            data["value"] = message + "\033[22m \033[39m"
        data["userID"] = user_data["userID"]
        data["password"] = user_data["password"]
        data["chatroom"] = chatroom
        data["alias"] = username
        json_data = json.dumps(data)
        return json_data

    def __init__(self, input_list, user_data, chatroom, username):
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
            self.output= self.send_message(input, input_list, errors, user_data, chatroom, username)

    def to_json(self):
		return self.output
