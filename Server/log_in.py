#!/usr/bin/python
import sys
import re
import os
import urlparse
import psycopg2

#postgresql db hosted online
con = psycopg2.connect(
    database="d8949uhaqoqd28",
    user="gmultvozsunwxb",
    password="6b0f18a546857583252b8da92d3dfcbc811de51fc3ace445b3f972e35aba2f7f",
    host="ec2-54-225-236-102.compute-1.amazonaws.com",
    port=5432
)

cur =con.cursor()


#insert username and password into db
def sign_up(username,password):
    cur.execute("INSERT INTO log_in(username, password) VALUES(%s,%s);",(username,password))
    
# match username and password in db. If match login. If password is not match, retype password(user) or create username.
def signup_or_login(username,password):
    cur.execute("SELECT * FROM log_in WHERE username=%s and password=%s",(username,password))
    found =cur.fetchone()
    if (found):
        print "log in successful!"    
    else:  
        signUP= raw_input('wrong password, do you want to sign up?[Y or N]: ')
        if (signUP=="Y"):   
            username=input_name() 
            print username
            password= raw_input('password: ')
            sign_up(username,password)
            print "^.^ Welcome new user!"
        else:
            password= raw_input('password: ')
            signup_or_login(username,password)


          
#check the format of the username
def validate_username(username):
    re1='((^[a-zA-Z0-9]*$))'
    rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
    m = rg.search(username)
    if m:
        return True
    print "please no special charactors or space"
    return False


#check if the user name is in db
def exists_username(username):
    cur.execute("SELECT username FROM log_in")
    rows=cur.fetchall()
    for row in rows:
        if row[0]==username:
            print "name is taken!"
            return False
    return True
      


# new user create username
def input_name():
    username =raw_input('username: ')    
    print exists_username(username)
    print validate_username(username)
    if (exists_username(username)==True and validate_username(username)==True):
        return username
    else:
        input_name()
       
       
   
def main():       
    username= raw_input('username: ') 
    password=raw_input('password: ')
    signup_or_login(username , password)       
    con.commit()
    con.close()


if __name__=="__main__":
    main()
