#!/usr/bin/python
import MySQLdb
import sys
import re




con=MySQLdb.connect(
    user ="root",
    passwd= "WWWWWWWWWW",
    host= "localhost",
    db= "log_in_sys" )
cur =con.cursor()
username =""


def sign_up(username,password):
    cur.execute("INSERT INTO log_in VALUE(%s,%s)",(username,password))
    

def signup_or_login(username,password):
    cur.execute("SELECT * FROM log_in WHERE username=%s and password=%s",(username,password))
    found =cur.fetchone()
    if (found):
        print "user exists!"        
    else:
       
        sign_up(username,password)
          

def validate_name(username):
    #if username
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
    username=input_name()
    password=raw_input('password: ')
    signup_or_login(username , password)        
    con.commit()
    con.close()

if __name__== "__main__":
    main()