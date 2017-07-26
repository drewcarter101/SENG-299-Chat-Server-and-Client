import socket 
import json 


class ServerWrapper:
    ServerLocation ='localhost'
    Port= 9321

    def __init__(self):

        self.connect(self.Port)
    

    def connect(self,port):
        try:
            self.s=socket.socket()
            host = socket.gethostname()
            self.s.connect((host,port))
        except IOError:
            print({'error':'connectionFailed'})
            return {'error':'connectionFailed'}



    def login(self,Username,Password):
        
        data={'requestType':'login', 'username': Username, 'password': Password} 
        return self.receive_and_parse(data)
        

    def signup(self,Username,Password):
    
        data = {'requestType':'signup', 'username': Username, 'password': Password}
        return self.receive_and_parse(data)
        
    
    def send(self,UserID,Password,Chatroom,Message):
        
        data = {'requestType':'send', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'message':Message}
        return self.receive_and_parse(data)
        
    
    def get(self,UserID,Password,Chatroom,LastUpdate=None):
        
        if LastUpdate is None:
            data = {'requestType':'get', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
            return self.receive_and_parse(data)
        else:
            data = {'requestType':'get', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'lastUpdate':LastUpdate}
            return self.receive_and_parse(data)
        
    
    def set_alias(self,UserID,Password,NewUsername):

        data = {'requestType':'set_alias', 'userID': UserID, 'password': Password,'newUsername':NewUsername}
        return self.receive_and_parse(data)
        

    def join(self,UserID,Password,Chatroom):
        
        data = {'requestType':'join', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        return self.receive_and_parse(data)
        

    def create(self,UserID,Password,Chatroom):
        
        data = {'requestType':'create', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        return self.receive_and_parse(data)
        

    def block(self,UserID,Password,UserToBlock,Chatroom):
    
        data = {'requestType':'block', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'userToBlock':UserToBlock}
        return self.receive_and_parse(data)
    

    def unblock(self,UserID,Password,UserToUnblock,Chatroom):
        
        data = {'requestType':'unblock', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'userToUnblock':UserToUnblock}
        return self.receive_and_parse(data)
        

    def delete(self,UserID,Password,Chatroom):
        
        data = {'requestType':'delete', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        return self.receive_and_parse(data)
        

    def receive_and_parse(self,data):
        
        request=json.dumps(data)
        self.s.send(request)
        reply=json.loads(self.s.recv(2048))
        self.s.close()
        print reply
        return reply 
        
