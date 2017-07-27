import unittest
from ServerWrapper import *



class Test_Authenticator(unittest.TestCase):

    def test_signup_login(self):
        test= ServerWrapper('localhost')
        self.assertIsInstance(test.signup('98','6789'),int)
        test2=ServerWrapper('localhost')
        self.assertIsInstance(test2.login('98','6789'),int)
    
    def test_send(self):
        test= ServerWrapper('localhost')
        user_id=test.signup('c','d')
        test2=ServerWrapper('localhost')
        self.assertEqual(test2.send( user_id,'d','general','hello'),True)
    
    def test_get(self):
        test= ServerWrapper('localhost')
        user_id=test.signup('e','f')
        test2=ServerWrapper('localhost')
        test2.send( user_id,'f','general','hello')
        test3=ServerWrapper('localhost')
        self.assertIsInstance(test3.get( user_id,'f','general'),list) 
        test4=ServerWrapper('localhost')
        test4.send( user_id,'f','general','bye')
        test5=ServerWrapper('localhost')
        self.assertIsInstance(test5.get( user_id,'f','general',0),list)   
    
    
    def test_set_alias(self):
        test= ServerWrapper('localhost')
        user_id=test.signup('h','i')
        test2=ServerWrapper('localhost')
        self.assertEqual(test2.set_alias(user_id,'i','hh'),True)
      
   
    def test_join(self):
        test= ServerWrapper('localhost')
        user_id1=test.signup('l','k')
        test2=ServerWrapper('localhost')
        user_id2=test2.signup('12','15')
        test3=ServerWrapper('localhost')
        test3.create(user_id1,'k','roomj')
        test4=ServerWrapper('localhost')
        self.assertEqual(test4.join( user_id2,'15','roomj'),True)
       
   
    def test_create(self):
        test= ServerWrapper('localhost')
        user_id_create=test.signup('a','b')
        test2=ServerWrapper('localhost')
        self.assertEqual(test2.create(user_id_create,'b','roomc'),True)

    def test_block(self):
        test= ServerWrapper('localhost')
        test.signup('lily','lon')
        test1= ServerWrapper('localhost')
        user_id_block=test1.signup('windy','bon')
        test2= ServerWrapper('localhost')
        test2.create(user_id_block,'bon','roomb')
        test3=ServerWrapper('localhost')
        self.assertEqual(test3.block(user_id_block,'bon','lily','roomb'),True)

    def test_unblock(self):
        test= ServerWrapper('localhost')
        user_id=test.signup('vi','kon')
        test1= ServerWrapper('localhost')
        test1.signup('wow','pon')
        test2= ServerWrapper('localhost')
        test2.create(user_id,'kon','roomu')
        test3=ServerWrapper('localhost')
        test3.block(user_id,'kon','wow','roomu')
        test4=ServerWrapper('localhost')
        self.assertEqual(test4.unblock(user_id,'kon','wow','roomu'),True)


    def test_delete(self):
        test= ServerWrapper('localhost')
        user_id=test.signup('willow','butter')
        test2= ServerWrapper('localhost')
        test2.create(user_id,'butter','roomd')
        test3=ServerWrapper('localhost')
        self.assertEqual(test3.delete( user_id,'butter','roomd'),True)



if __name__=='__main__':
    unittest.main(exit=False)