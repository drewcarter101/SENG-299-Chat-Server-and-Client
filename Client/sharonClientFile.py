#!/usr/bin/python

import socket
import tkinter as tk

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.name_bar = tk.Entry(self)
        self.name_bar.pack(side="top")

        self.input_bar = tk.Entry(self)
        self.input_bar.pack(side="left")

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Send"
        self.hi_there["command"] = self.send_msg
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

        

    def send_msg(self):
        s = socket.socket()
        host = socket.gethostname()
        port = 9999
        

        address = (host, port)
        msg=self.name_bar.get() + ": " +self.input_bar.get()
        self.input_bar.delete(0, len(msg))

        s.connect(address)
        s.send(msg.encode())

root = tk.Tk()
app = Application(master=root)
app.mainloop()