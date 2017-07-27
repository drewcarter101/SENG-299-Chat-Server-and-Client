import socket 
import json 
from Message import Message 

class ServerWrapper:
    ServerLocation ='localhost'
    Port= 9321

    def __init__(self):
        self.connect(self.Port)
    

    def connect(self,port):
        try:
            self.s=socket.socket()
           #host = socket.gethostname()
            host=socket.gethostbyname(self.ServerLocation)
            self.s.connect((host,port))
        except IOError:
            raise connectionFailedException 
            

    def login(self,Username,Password):
        data={'requestType':'login', 'username': Username, 'password': Password} 
        reply=self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
            
            return reply["userID"]
        
        else:
            
            return self.exceptions(outcome)
        

    def signup(self,Username,Password):
    
        data = {'requestType':'signup', 'username': Username, 'password': Password}
        reply=self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
            return reply["userID"]
        else:
            return self.exceptions(outcome)
    
    def send(self,UserID,Password,Chatroom,Message):
        
        data = {'requestType':'send', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'message':Message}
        reply=self.receive_and_parse(data)  
        outcome=reply["responseType"]
        if outcome =="Ok":
            return True
        else:
            return self.exceptions(outcome)
    
    def get(self,UserID,Password,Chatroom,LastUpdate=None):
    
        if LastUpdate is None:
            data = {'requestType':'get', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        else:
            data = {'requestType':'get', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'lastUpdate':LastUpdate}
      
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        lastUpdate=reply['lastUpdate']
        if outcome =="Ok":

            message_list=[]
            for item in reply["messages"]:
                message=Message(item["username"],item["text"])           
                message_list.append(message) 
            return (lastUpdate,message_list)   
        else:
            return self.exceptions(outcome)
           
    
    def set_alias(self,UserID,Password,NewUsername):

        data = {'requestType':'set_alias', 'userID': UserID, 'password': Password,'newUsername':NewUsername}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def join(self,UserID,Password,Chatroom):
        
        data = {'requestType':'join', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def create(self,UserID,Password,Chatroom):
        
        data = {'requestType':'create', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def block(self,UserID,Password,UserToBlock,Chatroom):
    
        data = {'requestType':'block', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'userToBlock':UserToBlock}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
    

    def unblock(self,UserID,Password,UserToUnblock,Chatroom):
        
        data = {'requestType':'unblock', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'userToUnblock':UserToUnblock}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def delete(self,UserID,Password,Chatroom):
        
        data = {'requestType':'delete', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def receive_and_parse(self,data):
        try:
            request=json.dumps(data)
            self.s.send(request)
            reply=json.loads(self.s.recv(2048))
            self.s.close()
            return reply 
        except Exception:
            raise failed_recv_Exception

    def exceptions(self,string):
        if string =='requestTypeMissing':
            raise requestTypeMissingException
        elif string =='requestFormatError':
            raise requestFormatErrorException 
        elif string == 'duplicateUsername':
            raise duplicateUsernameException
        elif string == 'invalidUsername':
            raise invalidUsernameException
        elif string=='invalidPassword':
            raise invalidPasswordException
        elif string=='parametersMissing':
            raise parametersMissingException 
        elif string=='invalidCredentials':
            raise invalidCredentialsException
        elif string=='invalidMessage':
            raise invalidMessageException
        elif string=='chatroomDoesNotExist':
            raise chatroomDoesNotExistException
        elif string=='duplicateChatrooom':
            raise duplicateChatrooomException
        elif string=='userDoesNotExist':
            raise userDoesNotExistException
        elif string=='notOwner':
            raise notOwnerException
        elif string=='userNotOnList':
            raise userNotOnListException 
        elif string=='parameterFormatError':
            raise parameterFormatErrorException
        elif string=='invalidChatroom':
            raise invalidChatroomException
        elif string =='bloked':
            raise blockedException
        else:
            raise undefinedException




class connectionFailedException(Exception):
    pass

class failed_recv_Exception(Exception):
    pass

class undefinedException(Exception):
    pass

class blockedException(Exception):
    pass

class requestTypeMissingException(Exception):
    pass
    
class requestFormatErrorException(Exception):
    pass

class duplicateUsernameException(Exception):
    pass

class invalidUsernameException(Exception):
    pass

class invalidPasswordException(Exception):
    pass

class parametersMissingException(Exception):
    pass

class invalidCredentialsException(Exception):
    pass

class invalidMessageException(Exception):
    pass

class chatroomDoesNotExistException(Exception):
    pass

class duplicateChatrooomException(Exception):
    pass

class userDoesNotExistException(Exception):
    pass

class notOwnerException(Exception):
    pass

class userNotOnListException(Exception):
    pass

class parameterFormatErrorException(Exception):
    pass

class invalidChatroomException(Exception):
    pass


#user=ServerWrapper()
#user.signup('1234','4321')
#user.send(0,'4321','general','ccc')


#ser.get(0,'4321','general',1)


