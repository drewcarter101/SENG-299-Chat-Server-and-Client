
import sys
import os
import re
import json
from formatter import InpuHandler


credentials={}
newUser=False
credential_errors={"invalid_username": "Username must...", "invalid password": "Password must be...", "Invalid pairing": "The password entered does not match the username"}#fill in later
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
    helpText=myfile.read()

def usernameValid(username):
    data={"type":"login_command", "function": "validate_nameFormat({})".format(username)} #called in server by valid=eval(data["function"]), valid is what is returned, I know eval is kinda bad
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    return True

def usernameExists(username):
    data={"type":"login_command", "function": "validate_name({})".format(username)} #called in server by valid=eval(data["function"]), valid is what is returned, I know eval is kinda bad
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    return True

def passwordValid(password):
    #fill in later
    return True

def passwordMatch(username, password):
    #need method in login
    return True

def sign_up(username,password):
    data={"type":"login_command", "function": "sign_up({},{})".format(username, password)}
    json_data = json.dumps(data)
    #send json_data to server
    #wait for response, return response
    return

def peformAction(command, value):
    if command=="set_alias":
        credentials["username"]=value  
    elif command== "help":
        print helpText
    elif command =="quit":
        sys.exit()
    return


#Prompt user for username
print "Welcome"
while True:
    tempUser = raw_input("Please enter your chosen username: \n\n")#wait for user to enter username
    if usernameValid(tempUser):#check if user name is valid, if not valid start loop again
        if usernameExists(tempUser):#check if username exists in database
            response = raw_input("Type 'y' to confirm username as{}, type anything else to re-enter: \n\n".format(tempUser))
            if response == "y":    
                credentials["username"]=tempUser #if it exists, set username
                break  #stops the loop
        else:#if it doesn't exist
            print "Username does not exist"
            response = raw_input("Type 's' to signup, press any key to try again\n\n")
            if response == "s":
                print "Beginning sign up process..."
                newUser=True
                credentials["username"]=tempUser
                break
    else:
        print credential_errors["invalid_username"]

#Check password
while True:
    tempPass = raw_input("please enter your password: " + credential_errors["invalid password"]+ "\n\n")
    if passwordValid(tempPass):
        if newUser:
            credentials["password"]=tempPass
            sign_up(credentials["username"], credentials["password"])
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
  
print "What do you want to do now?"
while True: #Main Program loop
    input_list= raw_input()
    parser=InpuHandler(input_list.split(" "), credentials)
    output= json.loads(parser.to_json())
    if output["type"]=="client_command":
        peformAction(output["command"], output["value"])
    #else send output to server to decide what to do next
    print(output)