#!/usr/bin/env python

import sys
import re
import json
import os
from ServerWrapper import *
from Chat import Chat
from ClientStateInfo import ClientStateInfo
from Constant import GENERAL_CHATROOM
from Credentials import *

class Start():
	
	## Constructor initiates variables and starts program
	def __init__(self):
		#Help text
		__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
			self.helpText=myfile.read()
			
		self.credential_errors={"Ok": "Success","InvalidUsername": "Usernames are alphanumeric and cannot be blank", "InvalidPassword": "Passwords are alphanumeric and cannot be blank", 
		"Invalid_pairing": "Either the password or username entered is incorrect", "DuplicateUsername": "This user name already exists, please enter a valid username", 
		"ParametersMissing" : "Blank entries are not allowed"}
		
		self.wrapper=ServerWrapper(sys.argv)
		
		self.run()
	
	## Starts login and sign up process and afterwards begins program
	def run(self):
		self.done=False
		print "Welcome! Type '/quit' to exit or '/help' for assistance."
		print "Login/sign-up below:\n"
		while True:
			tempUser=raw_input("Please enter a username: " + self.credential_errors["InvalidUsername"]+ "\n")
			if tempUser=="/quit":
				self.quit()
			elif tempUser=="/help":
				print self.helpText
				continue
			
			tempPass=raw_input("Please enter your password, if your account does not exist, you will be prompted to sign up: " + self.credential_errors["InvalidPassword"]+ "\n")
			if tempPass=="/quit":
				self.quit()
			elif tempPass=="/help":
				print self.helpText
				continue
				
			try:
				self.userId=self.wrapper.login(tempUser, tempPass) 
				print "Login complete!"
				break
			except (invalidCredentialsException, parametersMissingException, ServerWrapperException) as ex:
				if type(ex) == invalidCredentialsException:
					print self.credential_errors["Invalid_pairing"]
				elif type(ex) == parametersMissingException:
					print self.credential_errors["ParametersMissing"]
				else:
					print "Error occured while trying to perform operation"
					

				while True:
					response= raw_input("Press 's' to sign up as a new user with the credentials you enetered or press any key to retry login\n")
					if response== 's':
						print "Beginnng sign up process..."
						try:
								self.userId = self.wrapper.signup(tempUser, tempPass)
								print "Sign up complete, you are now logged in"
								self.done=True
								break
						except (duplicateUsernameException, invalidUsernameException, invalidPasswordException, parametersMissingException, ServerWrapperException) as exx:
							if type(ex) == duplicateUsernameException:
								print self.credential_errors["DuplicateUsername"]
							elif type(ex) == invalidUsernameException:
								print self.credential_errors["InvalidUsername"]
							elif type(ex) == invalidPasswordException:
								print self.credential_errors["InvalidPassword"]
							elif type(ex) == ServerWrapperException:
								print "Error occured while trying to perform operation"
							else:
								print self.credential_errors["ParametersMissing"]
					elif response=="/quit":
						self.quit()
					elif response=="/help":
						print self.helpText
						continue
					else:
						break
				if self.done:
					break
				
		print self.helpText
		print "This guide can be accessed again with the /help command\n"
		self.cred= Credentials(self.userId, tempPass)
		self.chat=Chat(self.cred, self.wrapper)
		self.chat.run()
		
	## Quits program
	def quit(self):
		sys.exit()
		
if __name__ == "__main__":
    start=Start()
