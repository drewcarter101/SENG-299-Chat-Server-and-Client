
import sys
import re
import json

credentials={}
newUser=False


def usernameValid(username):
    #check if username is valid, return True or False
    return True
    #Sharon: I'll fill this in later

def usernameExists(username):
    #check if username exists, return True or False
    return True
    #return Log_in.checkIfUsernameExists(username)

#sys.argv[1]
#Prompt user for username
print "Welcome"
while True:
    tempUser = raw_input("Please enter your chosen username\n\n")#wait for user to enter username
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
        print "Username must have..."#fill in later

