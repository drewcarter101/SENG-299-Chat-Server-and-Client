import socket 
import json 
from Message import Message 

class ServerWrapper:
    ServerLocation ='localhost'
    Port= 9321

    def __init__(self, location):
        self.ServerLocation = location

            

    def login(self,Username,Password):
        try:
            data={'requestType':'login', 'username': Username, 'password': Password} 
            reply=self.receive_and_parse(data)
            outcome=reply["responseType"]
            if outcome =="Ok":            
                return reply["userID"]
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def signup(self,Username,Password):
        try:
            data = {'requestType':'signup', 'username': Username, 'password': Password}
            reply=self.receive_and_parse(data)
            outcome=reply["responseType"]
            if outcome =="Ok":
                return reply["userID"]
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def send(self,UserID,Password,Chatroom,Message):
        try:
            data = {'requestType':'send', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'message':Message}
            reply=self.receive_and_parse(data)  
            outcome=reply["responseType"]
            if outcome =="Ok":
                return True
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def get(self,UserID,Password,Chatroom,LastUpdate=None):
        try:
            if LastUpdate is None:
                data = {'requestType':'get', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
            else:
                data = {'requestType':'get', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'lastUpdate':LastUpdate}
      
            reply= self.receive_and_parse(data)
            outcome=reply["responseType"]

            if outcome =="Ok":
                lastUpdate = reply['lastUpdate']
                message_list=[]
                for item in reply["messages"]:
                    message=Message(item["username"],item["text"])           
                    message_list.append(message) 
                return (lastUpdate,message_list)   
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 
    

    def set_alias(self,UserID,Password,NewUsername):
        try:
            data = {'requestType':'set_alias', 'userID': UserID, 'password': Password,'newUsername':NewUsername}
            reply= self.receive_and_parse(data)
            outcome=reply["responseType"]
            if outcome =="Ok":
                return True
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def join(self,UserID,Password,Chatroom):
        try:
            data = {'requestType':'join', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
            reply= self.receive_and_parse(data)
            outcome=reply["responseType"]
            if outcome =="Ok":
                return True
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def create(self,UserID,Password,Chatroom):
        try:
            data = {'requestType':'create', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
            reply= self.receive_and_parse(data)
            outcome=reply["responseType"]
            if outcome =="Ok":
                return True
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def block(self,UserID,Password,UserToBlock,Chatroom):
        try:
            data = {'requestType':'block', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'userToBlock':UserToBlock}
            reply= self.receive_and_parse(data)
            outcome=reply["responseType"]
            if outcome =="Ok":
                return True
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def unblock(self,UserID,Password,UserToUnblock,Chatroom):
        try:
            data = {'requestType':'unblock', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'userToUnblock':UserToUnblock}
            reply= self.receive_and_parse(data)
            outcome=reply["responseType"]
            if outcome =="Ok":
                return True
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def delete(self,UserID,Password,Chatroom):
        try:
            data = {'requestType':'delete', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
            reply= self.receive_and_parse(data)
            outcome=reply["responseType"]
        
            if outcome =="Ok":
                return True
            else:
                return self.exceptions(outcome)
        except KeyError:
            raise BadResponseException 


    def receive_and_parse(self,data):
        try:
            s = socket.socket()
            requestString = json.dumps(data)

            host = socket.gethostname()
            #host=socket.gethostbyname('localhost')
            port = 9321

            s.connect((host, port))
            s.send(requestString)

            #print data

            response = s.recv(2048)
            #print response
            return json.loads(response)

        except Exception:
            raise failed_recv_Exception


    def exceptions(self,string):
        if string =='RequestTypeMissing':
            raise requestTypeMissingException
        elif string =='RequestFormatError':
            raise requestFormatErrorException 
        elif string == 'DuplicateUsername':
            raise duplicateUsernameException
        elif string == 'InvalidUsername':
            raise invalidUsernameException
        elif string=='InvalidPassword':
            raise invalidPasswordException
        elif string=='ParametersMissing':
            raise parametersMissingException 
        elif string=='InvalidCredentials':
            raise invalidCredentialsException
        elif string=='InvalidMessage':
            raise invalidMessageException
        elif string=='ChatroomDoesNotExist':
            raise chatroomDoesNotExistException
        elif string=='DuplicateChatrooom':
            raise duplicateChatrooomException
        elif string=='UserDoesNotExist':
            raise userDoesNotExistException
        elif string=='NotOwner':
            raise notOwnerException
        elif string=='UserNotOnList':
            raise userNotOnListException 
        elif string=='ParameterFormatError':
            raise parameterFormatErrorException
        elif string=='InvalidChatroom':
            raise invalidChatroomException
        elif string =='Blocked':
            raise blockedException
        else:
            raise undefinedException




class ServerWrapperException(Exception):
    pass

class BadResponseException(ServerWrapperException):
    pass

class failed_recv_Exception(ServerWrapperException):
    pass

class undefinedException(ServerWrapperException):
    pass

class blockedException(ServerWrapperException):
    pass

class requestTypeMissingException(ServerWrapperException):
    pass
    
class requestFormatErrorException(ServerWrapperException):
    pass

class duplicateUsernameException(ServerWrapperException):
    pass

class invalidUsernameException(ServerWrapperException):
    pass

class invalidPasswordException(ServerWrapperException):
    pass

class parametersMissingException(ServerWrapperException):
    pass

class invalidCredentialsException(ServerWrapperException):
    pass

class invalidMessageException(ServerWrapperException):
    pass

class chatroomDoesNotExistException(ServerWrapperException):
    pass

class duplicateChatrooomException(ServerWrapperException):
    pass

class userDoesNotExistException(ServerWrapperException):
    pass

class notOwnerException(ServerWrapperException):
    pass

class userNotOnListException(ServerWrapperException):
    pass

class parameterFormatErrorException(ServerWrapperException):
    pass

class invalidChatroomException(ServerWrapperException):
    pass


#user=ServerWrapper()
#user.signup('1234','4321')
#user.send(0,'4321','general','ccc')


#ser.get(0,'4321','general',1)


