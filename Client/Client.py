
import sys
import os
import re
import json
from formatter import InpuHandler


credentials={}
firstTry=True
credential_errors={"InvalidUsername": "Username must...", "InvalidPassword": "Password must be...", "Invalid_pairing": "Either the password or username entered is incorrect", "DuplicateUsername": "This user name already exists, please enter a valid username"}#fill in later
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
    helpText=myfile.read()

def sign_up(username,password):
    data={"type":"db_command", "ID": "signup", "username": username, "password": password }
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    return "test"

def login(username,password):
    data={"type":"db_command", "ID": "login", "username": username, "password": password }
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    return "Ok"

def set_alias(username, password, newUsername):
    data={"type":"db_command", "ID": "set_alias", "username": username, "password": password, "newUsername": newUsername }
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    return

def peformAction(command, value):
    if command=="set_alias":
        tempUser=  raw_input("please re-enter your username: \n")
        tempPass=  raw_input("please re-enter your password: \n")
        tempNewUser=  raw_input("please enter your new username: \n")
        set_alias(tempUser, tempPass, tempNewUser)
    elif command== "help":
        print helpText
    elif command =="quit":
        sys.exit()
    return


#Prompt user for username
print "Welcome"
while True:
    tempUser=raw_input("please enter a username: " + credential_errors["InvalidUsername"]+ "\n")
    tempPass=raw_input("please enter your password: " + credential_errors["InvalidPassword"]+ "\n")
    if login(tempUser, tempPass) and firstTry == "Ok":
        print "Login complete!"
        break
    elif login(tempUser, tempPass) == "InvalidCredentials":
        if firstTry: print credential_errors["Invalid_pairing"]
        response= raw_input("Press 's' to sign up as a new user or press any key to retry login\n")
        if response== 's':
            firstTry=False
            print "Beginnng sign up process..."
            if sign_up(tempUser, tempPass)=="Ok":
                print "Sign up complete, you are now logged in"
                break
            else:
                print credential_errors[sign_up(tempUser, tempPass)]

print "What do you want to do now?"
while True: #Main Program loop
    input_list= raw_input()
    parser=InpuHandler(input_list.split(" "), credentials)
    output= json.loads(parser.to_json())
    if output["type"]=="client_command":
        peformAction(output["command"], output["value"])
    #else send output to server to decide what to do next
    print(output)