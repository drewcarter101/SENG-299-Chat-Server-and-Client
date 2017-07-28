from MessageUpdater import MessageUpdater
from ClientStateInfo import ClientStateInfo
from ServerWrapper import ServerWrapper
from Credentials import Credentials
from InputHandler import InputHandler
import socket
import time


serverWrapper = ServerWrapper('127.0.0.1')
clientStateInfo = ClientStateInfo(Credentials(0,'password'),'handlerChat')
inputHandler = InputHandler(serverWrapper,clientStateInfo,None)

inputHandler.run()
time.sleep(5)
inputHandler.quit()