from log_in import dbHandler
from User import User
import unittest 

class Test_log_in(unittest.TestCase):
    def setUp(self):
        self.db = dbHandler("d8949uhaqoqd28","gmultvozsunwxb",
        "6b0f18a546857583252b8da92d3dfcbc811de51fc3ace445b3f972e35aba2f7f",
        "ec2-54-225-236-102.compute-1.amazonaws.com",5432)
               

    """ test for insert function  """
    def test_insert(self):
        self.assertEqual(self.db.insert('wrnsdsfgdsds','eeeeecfde'),22)
    
    """ test for finfByID function """
    def test_findByID(self):
        self.assertEqual(self.db.findByID(16).name,'weeen')

    """ test for finfByName function """
    def test_findByName(self):
         self.assertEqual(self.db.findByName('weeen').password,'eeeeynd')
     
    """ test for updateUser function """
    def test_updateUser(self):
        self.db.updateUser(12,'jas','lea')
        self.assertEqual(self.db.findByID(12).name,'jas')
        



if __name__=='__main__':
    unittest.main(exit=False)

