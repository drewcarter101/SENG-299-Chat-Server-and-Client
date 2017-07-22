#!/usr/bin/python
import sys
import re
import os
import urlparse
import psycopg2
import logging
from User import User 



class dbHandler:


    def __init__(self,database,user,password,host,port):
        self.database=database
        self.user=user
        self.password=password 
        self.host=host
        self.port=port
        try:
            self.con = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
                )

            self.cur =self.con.cursor()
        
        except IOError as err:
            logging.error('functionName:%s',err)

        
    """insert user name and password into db, return id"""
    def insert(self,username,password):
        try:
            if type(username) != str or type(password)!=str:
                raise Exception
        except Exception :
            logging.error('name/password is a string')
  
        else: 
            cmd_1="INSERT INTO log_in(username, password) VALUES(%s,%s);"
            cmd_2="SELECT ID FROM log_in WHERE username =%s and password=%s;"
            self.cur.execute(cmd_1,(username,password))
            self.cur.execute(cmd_2,(username,password))
            a=self.cur.fetchone()  
            user_id=int(a[0])
           # self.con.commit()
            #self.con.close()
            return user_id
        

    """take id as input, return an instance of User"""
    def findByID(self,user_id):    
      
        cmd="SELECT username, password FROM log_in WHERE id=%s;"
        self.cur.execute(cmd,([user_id])) 
        properties=self.cur.fetchone() 
        if properties is None:
            return None
        else:
            the_user=User(properties[0],user_id,properties[1])  
          #  self.con.commit()
           # self.con.close()
            return the_user
     


    """take username as input, return an instance of User"""
    def findByName(self,username):

        cmd="SELECT id, password FROM log_in WHERE username=%s;"
        self.cur.execute(cmd,[username])
        properties=self.cur.fetchone()
        if properties is None:
            return None
        else:
            the_user=User(username,properties[0],properties[1])
          #  self.con.commit()
          #  self.con.close()
            return the_user 

    """ take id, new_username, new_password as input, no return """
    def updateUser(self,user_id,new_username,new_password):
        try:
             if type(new_username) != str or type(new_password)!=str:
                raise Exception
        except Exception :
            logging.error('name/password is a string')  
        else:
            cmd="UPDATE log_in SET username=%s, password=%s WHERE id=%s;"
            self.cur.execute(cmd, (new_username,new_password,user_id))           

            #self.con.commit()
            #self.con.close()




#db = dbHandler("d8949uhaqoqd28","gmultvozsunwxb","6b0f18a546857583252b8da92d3dfcbc811de51fc3ace445b3f972e35aba2f7f","ec2-54-225-236-102.compute-1.amazonaws.com",5432)
#db.findByID(10)
#db.insert('s','se')
#db.findByName('jam')
#db.updateUser(1,'we','yeah')
