#!/usr/bin/python
import MySQLdb
import sys
import re


con=MySQLdb.connect(
    user ="root",
    passwd= "wwwwwwwwwww",
    host= "localhost",
    db= "log_in_sys" )
cur =con.cursor()



def sign_up(username,password):
    cur.execute("INSERT INTO log_in VALUE(%s,%s)",(username,password))
    

def signup_or_login(username,password):
    cur.execute("SELECT * FROM log_in WHERE username=%s and password=%s",(username,password))
    found =cur.fetchone()
    if (found):
        print "log in successful!"    
    else:  
        signUP= raw_input('do you want to sign up?[Y or N]: ')
        if (signUP=="Y"):   
            username=input_name() 
            password= raw_input('password: ')
            sign_up(username,password)
            print "^.^ Welcom new user!"
          

def validate_name(username):
    cur.execute("SELECT * FROM log_in")
    rows=cur.fetchall()
    for row in rows:
        if row[0]==username:
            print "name is taken!"
            return True
    return False
      



def input_name():
    username=raw_input('username: ')    
    if (validate_name(username)==True):
        input_name()
    else:
        return username
      
   

def main():
    username= raw_input('username: ') 
    password=raw_input('password: ')
    signup_or_login(username , password)       
    con.commit()
    con.close()


if __name__== "__main__":
    main()