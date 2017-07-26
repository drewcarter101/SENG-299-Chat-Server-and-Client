import unittest
from ServerWrapper import ServerWrapper




class Test_Authenticator(unittest.TestCase):
    def test_connection(self):
        test= ServerWrapper()
        test.Port=1234
        self.assertEqual(test.connect(test.Port),{'error':'connectionFailed'})

    def test_login(self):
        test= ServerWrapper()
        self.assertIsInstance(test.login('123','321'),dict)
    

    def test_signup(self):
        test= ServerWrapper()
        self.assertIsInstance(test.login('123','321'),dict)
    
    def test_send(self):
        test= ServerWrapper()
        self.assertIsInstance(test.send(0,'321','chatroom','hello'),dict)
    
    def test_get(self):
        test= ServerWrapper()
        self.assertIsInstance(test.get(0,'321','chatroom'),dict)
    
    def test_get_one_more_parameter(self):
        test= ServerWrapper()
        self.assertIsInstance(test.get(0,'321','chatroom',0),dict)
    
    def test_set_alias(self):
        test= ServerWrapper()
        self.assertIsInstance(test.set_alias(0,'321','1234'),dict)
   
    def test_join(self):
        test= ServerWrapper()
        self.assertIsInstance(test.join(0,'321','chatroom'),dict)
   
    def test_create(self):
        test= ServerWrapper()
        self.assertIsInstance(test.create(0,'321','chatroom'),dict)

    def test_block(self):
        test= ServerWrapper()
        self.assertIsInstance(test.block(0,'321','12345','chatroom'),dict)

    def test_unblock(self):
        test= ServerWrapper()
        self.assertIsInstance(test.unblock(0,'321','12345','chatroom'),dict)

    def test_delete(self):
        test= ServerWrapper()
        self.assertIsInstance(test.delete(0,'321','chatroom'),dict)



if __name__=='__main__':
    unittest.main(exit=False)