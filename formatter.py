#!/usr/bin/python

import sys
import re
import json

def send_command(commands):
    commands=list(filter(None, commands))
    data = {}
    data["command"] = commands[0]
    if len(commands)>1: data["names"]=commands[1]
    json_data = json.dumps(data)
    print(json_data)


chatroom_commands =["join","create","set_alias","block", "unblock", "delete", "help", "quit"]
input_list=sys.argv[1:]
formats={"/b":"", "b/": " ", "/i": " ", "i/": " ", "/u": " ", "u/": " ", "/h": " ", "h/": " ", "/happy": u'\U0001f604', "/sad": u'\U0001F622', "/angry": u'\U0001F620', "/bored": u'\U0001F634', "/thumbsup": u'\U0001F44D', "/thumbsdown": u'\U0001F44E', "/highfive": u'\U0000270B'}
input=" ".join([formats.get(item, item) for item in input_list])
print(input)

pattern1="^/(?:({}))\[([A-Za-z0-9_]+)\]$".format("|".join(chatroom_commands))
pattern2="^/(?:({}))$".format("|".join(chatroom_commands[6:]))
general_pattern="(?:{}|{})".format(pattern1, pattern2)

command_input=re.search(general_pattern, input)
numOfGroups=re.compile(general_pattern).groups

if command_input is not None:
    send_command([command_input.group(1), command_input.group(2), command_input.group(3)])
else:
    print("Not a command")







