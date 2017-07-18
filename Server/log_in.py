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
            
        except Exception as err:
            logging.error('functionName:%s',err)
        
    """insert user name and password into db, return id"""
    def insert(self,username,password):
        try:
            self.cur.execute("INSERT INTO log_in(username, password) VALUES('%s','%s');"%(username,password))
            self.cur.execute("SELECT ID FROM log_in WHERE username ='%s' and password='%s';"%(username,password))
            a=self.cur.fetchone()
        
            self.id=int(a[0])
            
        except Exception as err:
            logging.error('functionName:%s',err)

        self.con.commit()
        self.con.close()
        return self.id
        

    """take id as input, return an instance of User"""
    def findByID(self,id):    
        try:
            self.cur.execute("SELECT username, password FROM log_in WHERE id=%s;",[id]) 
            properties=self.cur.fetchone()  
            self.user=User(properties[0],id,properties[1])
           
        except Exception as err:
             logging.error('functionName:%s',err)
    
        self.con.commit()
        self.con.close()
        return self.user


    """take username as input, return an instance of User"""
    def findByName(self,username):
        try:
            self.cur.execute("SELECT id, password FROM log_in WHERE username='%s';"%username)
            properties=self.cur.fetchone()
            self.user=User(username,properties[0],properties[1])
           
        except Exception as err:
            logging.error('functionName:%s',err)
    
        self.con.commit()
        self.con.close()
        return self.user 

    """ take id, new_username, new_password as input, no return """
    def updateUser(self,id,new_username,new_password):
        try:
            self.cur.execute("UPDATE log_in SET username='%s', password='%s' WHERE id=%s;"%(new_username,new_password,id))
        except Exception as err:
            logging.error('functionName:%s',err)   

        #self.con.commit()
        #self.con.close()



