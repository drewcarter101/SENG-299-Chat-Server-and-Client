import unittest
from ChatSystem import *
import time

class ChatSystemTest (unittest.TestCase):
    def testInit(self):
        chatSystem = ChatSystem()
        messages = chatSystem.getMessagesByTime('general','cam');

        assert(len(messages[1]), 0)

unittest.main()