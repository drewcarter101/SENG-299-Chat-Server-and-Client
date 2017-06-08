#!/usr/bin/python

import sys
import re
import json

class ParseMessage():

    def send_command(self, commands, user_data):
        commands=list(filter(None, commands))
        data = {}
        data["type"]="command"
        data["command"] = commands[0]
        if len(commands)>1: data["value"]=commands[1]
        data["user"] = user_data["username"]
        data["password"] = user_data["password"]
        json_data = json.dumps(data)
        return json_data

    def send_message(self, message, user_data):
        data = {}
        data["type"]="normal"
        data["message"] = message
        data["user"] = user_data["username"]
        data["password"] = user_data["password"]
        json_data = json.dumps(data)
        return json_data

    def __init__(self, input_list, user_data):
        chatroom_commands =["join","create","set_alias","block", "unblock", "delete", "help", "quit"]
        formats={"/b": '\033[1m', "b/": '\033[0m', "/i": "/", "i/": "/", "/u": '\033[4m', "u/": '\033[0m', "/h": '\033[91m', "h/": '\033[0m', "/happy": u'\U0001f604', "/sad": u'\U0001F622', "/angry": u'\U0001F620', "/bored": u'\U0001F634', "/thumbsup": u'\U0001F44D', "/thumbsdown": u'\U0001F44E', "/highfive": u'\U0000270B'}
        input=" ".join([formats.get(item, item) for item in input_list])

        pattern1="^/(?:({}))\[([A-Za-z0-9_]+)\]$".format("|".join(chatroom_commands))
        pattern2="^/(?:({}))$".format("|".join(chatroom_commands[6:])) 
        general_pattern="(?:{}|{})".format(pattern1, pattern2)

        command_input=re.search(general_pattern, input)

        
        if command_input is not None:
            self.output=self.send_command([command_input.group(1), command_input.group(2), command_input.group(3)], user_data)
        else:
            self.output= self.send_message(input, user_data)

    def to_json(self):
        return self.output



input_list=sys.argv[1:]
user_d={"username":"Jeff", "password": "turtles"}
output= json.loads(ParseMessage(input_list, user_d).to_json())
print(output)



