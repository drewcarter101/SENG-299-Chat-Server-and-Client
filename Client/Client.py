
import sys
import os
import re
import json
from formatter import InpuHandler


credentials={}
notTryingSignUp=True
credential_errors={"InvalidUsername": "Username must...", "InvalidPassword": "Password must be...", "Invalid_pairing": "Either the password or username entered is incorrect", "DuplicateUsername": "This user name already exists, please enter a valid username"}#fill in later
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
    helpText=myfile.read()

def sign_up(username,password):
    if "/quit" in [username, password]:
        sys.exit()
    data={"requestType": "signup", "username": username, "password": password }
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    return "Ok"

def login(username,password):
    if "/quit" in [username, password]:
        sys.exit()
    data={"requestType": "login", "username": username, "password": password }
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    return "Ok"

def set_alias(username, password, newUsername):
    data={"requestType": "set_alias", "username": username, "password": password, "newUsername": newUsername }
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    #   if succesful credential["username"]=value
    return "Name succesfully changed!"

def peformAction(command, value):
    if command=="set_alias":
        print set_alias(credentials["username"], credentials["password"], value)
    elif command== "help":
        print helpText
    elif command =="quit":
        sys.exit()
    return


#Prompt user for username
print "Welcome"
while True:
    tempUser=raw_input("please enter a username: " + credential_errors["InvalidUsername"]+ "\n")
    if tempUser=="/quit":
        sys.exit()
    tempPass=raw_input("please enter your password: " + credential_errors["InvalidPassword"]+ "\n")
    if login(tempUser, tempPass)== "Ok" and notTryingSignUp:
        credentials["username"]=tempUser
        credentials["password"]=tempPass
        print "Login complete!"
        break
    elif login(tempUser, tempPass) == "InvalidCredentials":
        if notTryingSignUp: print credential_errors["Invalid_pairing"]
        response= raw_input("Press 's' to sign up as a new user or press any key to retry login\n")
        if response== 's':
            notTryingSignUp=False
            print "Beginnng sign up process..."
            if sign_up(tempUser, tempPass)=="Ok":
                credentials["username"]=tempUser
                credentials["password"]=tempPass
                print "Sign up complete, you are now logged in"
                break
            else:
                print credential_errors[sign_up(tempUser, tempPass)]
        elif response=="/quit":
            sys.exit()
    else: 
        print "Invalid entry"

print "What do you want to do now?"
while True: #Main Program loop
    input_list= raw_input()
    parser=InpuHandler(input_list.split(" "), credentials)
    output= json.loads(parser.to_json())
    if output["requestType"]=="client_command":
        peformAction(output["command"], output["value"])
    elif output["requestType"]=="error":
        print output["message"]
    else:
        #else send output to server to decide what to do next
        print(output["message"])