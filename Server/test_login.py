from log_in import dbHandler
from log_in import DuplicateNameException
from log_in import IDNotExistException
import urlparse
import psycopg2
import logging
import unittest 
from User import User 

class Test_log_in(unittest.TestCase):
    
    def truncate(self,db):
        connection= db.con
        cur=connection.cursor()
        cur.execute("truncate log_in;")
        connection.commit()
        cur.close()
      
    #""" test for insert function  """
    def test_insert(self):  

        db = dbHandler()
        self.truncate(db)
        self.assertIsInstance(db.insert('1234','4321'),int)
        db.close()
       
    def test_insert_Exception(self):
        
        db = dbHandler()
        self.truncate(db)
        self.assertIsInstance(db.insert('1234','4321'),int)
        self.assertRaises(DuplicateNameException,db.insert,'1234','4321')

    """ test for finfByID function """
    def test_findByID(self):
        db=dbHandler()
        self.truncate(db)
        db.insert('j','k')
        the_id=db.insert('m','l')
        db.insert('p','u')
        self.assertEqual(db.findByID(the_id).name,'m')
        self.assertEqual(db.findByID(the_id).password,'l')
        db.close()
#
    """ test for finfByName function """
    def test_findByName(self):
        db=dbHandler()
        self.truncate(db)
        db.insert('j','k')
        the_id=db.insert('m','l')
        db.insert('p','u')
        self.assertEqual(db.findByName('m').id,the_id)
        self.assertEqual(db.findByName('m').password,'l')
        db.close()
     
    """ test for updateUser function """
    def test_updateUser(self):
        db=dbHandler()
        self.truncate(db)
        the_id=db.insert('j','k')
        db.updateUser(the_id,'p','s')
        self.assertEqual(db.findByID(the_id).name,'p')
        self.assertEqual(db.findByID(the_id).password,'s')
        db.close()
   
    
    def test_updateUser_DuplicateNameException(self):
        db=dbHandler()
        self.truncate(db)
        db.insert('j','k')
        the_id=db.insert('u','o')
        self.assertRaises(DuplicateNameException,db.updateUser,the_id,'j','s')
        db.close()
    
    def test_updateUser_IDNotExistException(self):
        db=dbHandler()
        self.truncate(db)
        self.assertRaises(IDNotExistException,db.updateUser,1,'j','s')
        db.close()


if __name__=='__main__':
    unittest.main(exit=False)