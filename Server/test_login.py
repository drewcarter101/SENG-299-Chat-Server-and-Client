from DBHandler import *
#from DBHandlerImpl import DBHandlerImpl
from DBHandlerInMem import DBHandlerInMem
import unittest

class Test_log_in(unittest.TestCase):

    def getDBHandler(self):
        return DBHandlerInMem()

    def truncate(self,db):
        pass
        #if db is DBHandlerImpl:
            #connection= db.con
            #cur=connection.cursor()
            #cur.execute("truncate log_in;")
            #connection.commit()
            #cur.close()
      
    #""" test for insert function  """
    def test_insert(self):  

        db = self.getDBHandler()
        self.truncate(db)
        self.assertIsInstance(db.insert('1234','4321'),int)
        db.close()
       
    def test_insert_Exception(self):
        
        db = self.getDBHandler()
        self.truncate(db)
        self.assertIsInstance(db.insert('1234','4321'),int)
        self.assertRaises(DuplicateNameException,db.insert,'1234','4321')

    """ test for finfByID function """
    def test_findByID(self):
        db=self.getDBHandler()
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
        db=self.getDBHandler()
        self.truncate(db)
        db.insert('j','k')
        the_id=db.insert('m','l')
        db.insert('p','u')
        self.assertEqual(db.findByName('m').id,the_id)
        self.assertEqual(db.findByName('m').password,'l')
        db.close()
     
    """ test for updateUser function """
    def test_updateUser(self):
        db=self.getDBHandler()
        self.truncate(db)
        the_id=db.insert('j','k')
        db.updateUser(the_id,'p','s')
        self.assertEqual(db.findByID(the_id).name,'p')
        self.assertEqual(db.findByID(the_id).password,'s')
        db.close()
   
    
    def test_updateUser_DuplicateNameException(self):
        db=self.getDBHandler()
        self.truncate(db)
        db.insert('j','k')
        the_id=db.insert('u','o')
        self.assertRaises(DuplicateNameException,db.updateUser,the_id,'j','s')
        db.close()
    
    def test_updateUser_IDNotExistException(self):
        db=self.getDBHandler()
        self.truncate(db)
        self.assertRaises(IDNotExistException,db.updateUser,1,'j','s')
        db.close()


if __name__=='__main__':
    unittest.main(exit=False)