#!/usr/bin/env python

import sys
import re
import json
import os
from ServerWrapper import *
from Chat import Chat
from ClientStateInfo import ClientStateInfo

class Start():
	def __init__(self):
		#Help text
		__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		with open(os.path.join(__location__, "helpMsg.txt")) as myfile:
			self.helpText=myfile.read()
		self.credential_errors={"Ok": "Success","InvalidUsername": "Usernames are alphanumeric and cannot be blank", "InvalidPassword": "Passwords are alphanumeric and cannot be blank", "Invalid_pairing": "Either the password or username entered is incorrect", "DuplicateUsername": "This user name already exists, please enter a valid username", "ParametersMissing" : "ParametersMissing"}
		self.wrapper=ServerWrapper("location")
		self.notTryingSignUp=True
		
		print "Welcome! Type '/quit' to exit or '/help' for assistance."
		print "Login/sign-up below:\n"
		#login/signup screen
		while True:
			tempUser=raw_input("Please enter a username: " + self.credential_errors["InvalidUsername"]+ "\n")
			if tempUser=="/quit":
				self.quit()
			elif tempUser=="/help":
				print self.helpText
			
			tempPass=raw_input("Please enter your password, if your account does not exist, you will be prompted to sign up: " + self.credential_errors["InvalidPassword"]+ "\n")
			if tempPass=="/quit":
				self.quit()
			elif tempPass=="/help":
				print self.helpText
				
			try:
				if self.wrapper.login(tempUser, tempPass) and self.notTryingSignUp:
					print "Login complete!"
					break
			except ServerWrapperException:
				if self.notTryingSignUp:
					print self.credential_errors["Invalid_pairing"]
				response= raw_input("Press 's' to sign up as a new user or press any key to retry login\n")
				if response== 's':
					self.notTryingSignUp=False
					print "Beginnng sign up process..."
					try:
						if self.wrapper.signup(tempUser, tempPass):
							print "Sign up complete, you are now logged in"
							break
					except ServerWrapperException:
						print "An error has occured while attempting to perform the operation"
				elif response=="/quit":
					self.quit()
				elif response=="/help":
					print self.helpText
		
		
		self.chat=Chat((tempUser, tempPass), self.wrapper)
		self.chat.run()
		
	def quit(self):
		sys.exit()
