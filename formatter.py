#!/usr/bin/python

import sys
import re

def send_command(command, name, term):
    print(command, name, term)


chatroom_commands =["join","create","set_alias","block", "unblock", "delete", "help", "quit"]
input_list=sys.argv[1:]
input=",".join(input_list)

formats={"/b":"", "b/": " ", "/i": " ", "i/": " ", "/u": " ", "u/": " ", "/h": " ", "h/": " ", "/highfive": u'\U000270B'}

pattern1="/(?:({}))\[([A-Za-z0-9_]+)\]".format("|".join(chatroom_commands))
pattern2="/(?:({}))".format("|".join(chatroom_commands[6:]))
general_pattern="(?:{}|{})".format(pattern1, pattern2)

command_input=re.search(general_pattern, input)
print(command_input)
numOfGroups=re.compile(general_pattern).groups
print(numOfGroups)

if command_input is not None:
    send_command(command_input.group(1), command_input.group(2), command_input.group(3))
else:
    print("Not a command")







