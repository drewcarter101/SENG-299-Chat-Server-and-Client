from Authenticator import Authenticator
import unittest 

class Test_Authenticator(unittest.TestCase):
    
    def test_authenticateByID(self):
        auth = Authenticator()
        self.assertEqual(auth.authenticateByID(12),True)
        self.assertEqual(auth.authenticateByID(10000),False)

    def test_authenticateByName(self):
        auth = Authenticator()
        self.assertEqual(auth.authenticateByName('jam'),True)
        self.assertEqual(auth.authenticateByName('rubyy'),False)


if __name__=='__main__':
    unittest.main(exit=False)