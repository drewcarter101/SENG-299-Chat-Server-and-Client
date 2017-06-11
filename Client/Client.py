
import sys
import os
import re
import json
from formatter import ParseMessage


credentials={}
newUser=False
credential_errors={"invalid_username": "Username must...", "invalid password": "Password must be...", "Invalid pairing": "The password entered does not match the username"}#fill in later
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
    helpText=myfile.read()

def usernameValid(username):
    #check if username is valid, return True or False
    return True
    #Sharon: I'll fill this in later

def usernameExists(username):
    #check if username exists, return True or False
    return True
    #return Log_in.checkIfUsernameExists(username)

def passwordValid(password):
    return True

def passwordMatch(username, password):
    return True

def peformAction(command, value):
    if command=="set_alias":
        credentials["username"]=value  
    elif command== "help":
        print helpText
    elif command =="quit":
        sys.exit()
    return

#sys.argv[1]
#Prompt user for username
print "Welcome"
while True:
    tempUser = raw_input("Please enter your chosen username: \n\n")#wait for user to enter username
    if usernameValid(tempUser):#check if user name is valid, if not valid start loop again
        if usernameExists(tempUser):#check if username exists in database
            credentials["username"]=tempUser #if it exists, set username
            break  #stops the loop
        else:#if it doesn't exist
            print "Username does not exist"
            response = raw_input("Type 's' to signup, press any key to try again\n\n")
            if response == "s":
                print "Beginning sign up process..."
                newUser=True
                #signup user
                break
    else:
        print credential_errors["invalid_username"]

#Check password
while True:
    tempPass = raw_input("please enter your password: " + credential_errors["invalid password"]+ "\n\n")
    if passwordValid(tempPass):
        if newUser:
            credentials["password"]=tempPass
            #Enter new user into database
            print "Sign up complete! You are now logged in"
            break
        else:
            #Check if password matches username
            if passwordMatch(credentials["username"], tempPass):
                credentials["password"]=tempPass
                print "You are now logged in"
                break
            else:
                print credential_errors["Invalid pairing"]
    else:
        print tempPass + " is not a valid password"
  

while True: #Main Program loop
    input_list= raw_input("What do you want to do now?\n\n")
    parser=ParseMessage(input_list.split(" "), credentials)
    output= json.loads(parser.to_json())
    if output["type"]=="client_command":
        peformAction(output["command"], output["value"])
    print(output)
    break