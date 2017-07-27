from Authenticator import Authenticator
import unittest 
from log_in import dbHandler
import urlparse
import psycopg2
import logging
import unittest 
from User import User 

class Test_Authenticator(unittest.TestCase):
    
    def truncate(self,db):
        connection= db.con
        cur=connection.cursor()
        cur.execute("truncate log_in;")
        connection.commit()
        cur.close()

    def test_authenticateByID(self):
        db = dbHandler()
        self.truncate(db)
        the_id=db.insert('1234','4321')
        auth = Authenticator()   
        self.assertEqual(auth.authenticateByID(the_id,'4321'),True)
        self.assertEqual(auth.authenticateByID( the_id,'ok'),False)
        self.assertEqual(auth.authenticateByID(100,'1234'),False)

    def test_authenticateByName(self):
        db = dbHandler()
        self.truncate(db)
        db.insert('1234','4321')
        auth = Authenticator()
        self.assertEqual(auth.authenticateByName('1234','4321'),True)
        self.assertEqual(auth.authenticateByName('1234','1234'),False)
        self.assertEqual(auth.authenticateByName('no_such_name','4321'),False)

if __name__=='__main__':
    unittest.main(exit=False)