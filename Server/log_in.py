#!/usr/bin/python
import sys
import re
import os
import urlparse
import psycopg2
import logging
from User import User 



class dbHandler:
    def __init__(self):
        
        try:
            self.con = psycopg2.connect(
                database="d8949uhaqoqd28",
                user="gmultvozsunwxb",
                password="6b0f18a546857583252b8da92d3dfcbc811de51fc3ace445b3f972e35aba2f7f",
                host="ec2-54-225-236-102.compute-1.amazonaws.com",
                port=5432
                )

            self.cur =self.con.cursor()
            
        except Exception as err:
            logging.error('functionName:%s',err)
        

    def insert(self,username,password):
        try:
            self.cur.execute("INSERT INTO log_in(username, password) VALUES('%s','%s');"%(username,password))
            self.cur.execute("SELECT ID FROM log_in WHERE username ='%s' and password='%s';"%(username,password))
            a=self.cur.fetchone()
        
            self.id=int(a[0])
            #print(self.id)
            #return self.id #something wrong here, only when print the id, it will display in db

        except Exception as err:
            logging.error('functionName:%s',err)

        self.con.commit()
        self.con.close()
        return self.id


    def findByID(self,id):    
        try:
            self.cur.execute("SELECT username, password FROM log_in WHERE id=%s;",[id]) 
            properties=self.cur.fetchone()  
            self.user=User(properties[0],id,properties[1])
            #return self.user #it always return none

        except Exception as err:
             logging.error('functionName:%s',err)
    
        self.con.commit()
        self.con.close()
        return self.user


    def findByName(self,username):
        try:
            self.cur.execute("SELECT id, password FROM log_in WHERE username='%s';"%username)
            properties=self.cur.fetchone()
            self.user=User(username,properties[0],properties[1])
            #return self.user #always return none

        except Exception as err:
            logging.error('functionName:%s',err)
    
        self.con.commit()
        self.con.close()
        return self.user 


    def updateUser(self,id,new_username,new_password):
        try:
            self.cur.execute("UPDATE log_in SET username='%s', password='%s' WHERE id=%s;"%(username,password,id))
        except Exception as err:
            logging.error('functionName:%s',err)   

        self.con.commit()
        self.con.close()


#db = dbHandler()
#db.insert('wefsdfb','bddfgdfsdfj')
#db.findByID(14)
