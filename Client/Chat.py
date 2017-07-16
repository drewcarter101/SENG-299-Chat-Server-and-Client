
import sys
import os
import re
import json
from InputHandler import InputHandler
import Credentials as cred
import ClientStateInfo as csi

class Chat():
    ClientUsername=""

    messages={}
    notTryingSignUp=True

    credential_errors={"InvalidUsername": "Username must...", "InvalidPassword": "Password must be...", "Invalid_pairing": "Either the password or username entered is incorrect", "DuplicateUsername": "This user name already exists, please enter a valid username"}#fill in later
    
    #Help text
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
        helpText=myfile.read()

    def sign_up(self, username,password):
        #placeholder for method in serverwrapper
        return "Ok"

    def login(self, username,password):
        #placeholder for method in serverwrapper
        return "Ok"

    def set_alias(self, username, password, newUsername):
        #if bad
        ##return credential_Error[error message]
        #if successful change clientusername to newusername
        return "Name succesfully changed!\n"

    def peformAction(self, command, value):
        if command=="set_alias":
            print set_alias(cred.getCredentials()["userID"], cred.getCredentials()["password"], value)
        elif command== "help":
            print helpText
        elif command =="quit":
            quit()
        return

    def run(self):
        
        print "Welcome!"
        #login/signup screen
        while True:
            tempUser=raw_input("please enter a username: " + credential_errors["InvalidUsername"]+ "\n")
            if tempUser=="/quit":
                quit()
            tempPass=raw_input("please enter your password: " + credential_errors["InvalidPassword"]+ "\n")
            if tempUser=="/quit":
                quit()
            if login(tempUser, tempPass)== "Ok" and notTryingSignUp:
                ClientUsername=tempUser
                print "Login complete!"
                break
            elif login(tempUser, tempPass) == "InvalidCredentials":
                if notTryingSignUp: print credential_errors["Invalid_pairing"]
                response= raw_input("Press 's' to sign up as a new user or press any key to retry login\n")
                if response== 's':
                    notTryingSignUp=False
                    print "Beginnng sign up process..."
                    if sign_up(tempUser, tempPass)=="Ok":
                        ClientUsername=tempUser
                        print "Sign up complete, you are now logged in"
                        break
                    else:
                        print credential_errors[sign_up(tempUser, tempPass)]
                elif response=="/quit":
                    quit()
            else: 
                print "Invalid entry"

        #Main Program loop
        print "What do you want to do now?"
        while True: 
            input_list= raw_input()
            parser=InpuHandler(input_list.split(" "), cred.getCredentials(), csi.getCurrentChatroom())
            output= json.loads(parser.to_json())
            if output["Type"]=="client_command":
                peformAction(output["requestType"], output["value"])
            elif output["Type"]=="error":
                print output["value"]
            else:
                #else send output to server to decide what to do next
                #server_Send(output)
                #result=json.loads(server.recieve())
                #if result["requestType"]=="normal":
                    #add result["message"] to list of messages:
                    #messages[result["message"] ]="unseen"
                #else:
                    #print errors[result["message"]]
                print(output["value"])
            #result=json.loads(server.recieve())
            #if result["requestType"]=="normal":
                #add result["message"] to list of messages:
                #messages[result["message"] ]="unseen"
            #for key, value in messages.iteritems() :
                #if value=="unseen":
                    #print key
                    #value="seen"

    def quit(self):
        sys.exit()