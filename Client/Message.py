

class Message:
    def __init__(self, username, text):
        self.username = username
        self.text = text

    def __str__(self):
        return '[' + self.username + ']:' + ' ' + self.text