from log_in import dbHandler

import unittest 

class Test_log_in(unittest.TestCase):
    def setUp(self):

        self.database="d8949uhaqoqd28"
        self.user="gmultvozsunwxb"
        self.password= "6b0f18a546857583252b8da92d3dfcbc811de51fc3ace445b3f972e35aba2f7f"
        self.host="ec2-54-225-236-102.compute-1.amazonaws.com"
        self.port=5432

        self.db = dbHandler(self.database,self.user,self.password,self.host,self.port)
    

    """ test for insert function  """
    def test_insert(self):
        
        self.assertEqual(self.db.insert('west','1215'),18)

    
    """ test for finfByID function """
    def test_findByID(self):
    
        self.assertEqual(self.db.findByID(10).name,'we')

    """ test for finfByName function """
    def test_findByName(self):
         self.assertEqual(self.db.findByName('nick').password,'l2')
     
    """ test for updateUser function """
    def test_updateUser(self):
        self.db.updateUser(3,'yes','yess')
        self.assertEqual(self.db.findByID(3).name,'yes')
        



if __name__=='__main__':
    unittest.main(exit=False)

