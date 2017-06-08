#!/usr/bin/python

import socket
import tkinter as tk
from threading import Thread, Lock
import time

class ListenThread(Thread):

    def __init__(self, app, lock):
        Thread.__init__(self)
        self._app = app
        self._lock = lock
        self._terminating = False

    def destroy(self):
        self._terminating = True

    def run(self):
        s = socket.socket()
        host = socket.gethostname()
        port = 9999
        address = (host, port)

        s.connect(address)

        #def send_tst(msg):
            #s.send(msg)

        while True:

            if self._terminating:
                break

            if s.recv(1024).decode() != "":
                self._lock.acquire()
                self._app.post_new_data(s.recv(1024))
                self._lock.release()
            time.sleep(0.1)


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.root = tk.Tk()
        self._lock = Lock()
        self._listener = ListenThread(self, self._lock)
        #self._listener.start()
        self._listener.run()
        self.create_widgets()
        

    def create_widgets(self):
        #self._lock.acquire()
        # create a Frame for the Text and Scrollbar
        txt_frm = tk.Frame(self.root, width=300, height=600)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

    # create a Text widget

        self.name_bar = tk.Entry(txt_frm)
        self.name_bar.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.txt = tk.Text(txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        self.input_bar = tk.Entry(txt_frm)
        #self.input_bar.pack(side="left")
        self.input_bar.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)

        self.hi_there = tk.Button(txt_frm)
        self.hi_there["text"] = "Send"
        self.hi_there["command"] = self.send_msg
        #self.hi_there.pack(side="right")
        self.hi_there.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)

        self.quit = tk.Button(txt_frm, text="QUIT", fg="red",
                              command=root.destroy)
        #self.quit.pack(side="bottom")
        self.quit.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)

    # create a Scrollbar and associate it with txt
        scrollb = tk.Scrollbar(txt_frm, command=self.txt.yview)
        scrollb.grid(row=1, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set
        #self._lock.release()
        

   #def sendt_msg(self):
        #msg=self.name_bar.get() + ": " +self.input_bar.get()
        #self.input_bar.delete(0, len(msg))
        #self.send(msg.encode())

    def send_msg(self):
        s = socket.socket()
        host = socket.gethostname()
        port = 9999
        

        address = (host, port)
        msg=self.name_bar.get() + ": " +self.input_bar.get()
        self.input_bar.delete(0, len(msg))

        s.connect(address)
        s.send(msg.encode())
        #self.txt.insert(tk.END, s.recv(1024))
        #self.txt.insert(tk.END, "\n")     

    def post_new_data(self, data):
        self.txt.insert(tk.END, data)

    def all_data(self):
        self._lock.acquire()
        # ...
        self._lock.release()

    def destroy(self):
        self._listener.destroy()

root = tk.Tk()
app = Application(master=root)
app.mainloop()