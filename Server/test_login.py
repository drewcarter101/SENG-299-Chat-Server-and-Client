from log_in import dbHandler
from User import User
import psycopg2
import unittest 

class Test_log_in(unittest.TestCase):
    def setUp(self):

        self.db = dbHandler()
               

    """ test for insert function  """
    def test_insert(self):
        self.assertEqual(self.db.insert('weeen','eeeeynd'),16)
    
    """ test for finfByID function """
    def test_findByID(self):
        self.assertEqual(self.db.findByID(16).name,'weeen')

    """ test for finfByName function """
    def test_findByName(self):
         self.assertEqual(self.db.findByName('weeen').password,'eeeeynd')
     
    """ test for updateUser function """
  #  def test_updateUser(self):




if __name__=='__main__':
    unittest.main(exit=False)