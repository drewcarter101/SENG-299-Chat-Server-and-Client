from Authenticator import Authenticator
import unittest 

class Test_Authenticator(unittest.TestCase):
    
    def test_authenticateByID(self):
        auth = Authenticator()
       
        self.assertEqual(auth.authenticateByID(10,'yeah'),True)
        self.assertEqual(auth.authenticateByID(10,'ok'),False)
        self.assertEqual(auth.authenticateByID(100,'yeah'),False)

    def test_authenticateByName(self):
        auth = Authenticator()
        self.assertEqual(auth.authenticateByName('yes','yess'),True)
        self.assertEqual(auth.authenticateByName('yes','no'),False)
        self.assertEqual(auth.authenticateByName('no_such_name','yess'),False)

if __name__=='__main__':
    unittest.main(exit=False)