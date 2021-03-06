#!/usr/bin/env python

import Tkinter, sys
from Tkconstants import DISABLED, NORMAL
import socket 
import select 
import sys 
import io


class Get_in:

  def __init__(self):
    self.root = Tkinter.Tk()
    self.root.geometry("250x230")
    self.root.resizable(False, False)
#     self.login_user = []
    self.global_password = '123456'
    self.create()

  def check(self, event):
    nick = self.nickname_1.get()
    password = self.password_1.get()
    if nick == '':
      self.error_nick = Tkinter.Label(self.root, text = "Wrong nick", font = ("Red", 9))
      self.error_nick.place(x = 30, y = 80, height = 15)
    elif password != self.global_password:
      self.error_password = Tkinter.Label(self.root, text = "Wrong password", font = ("red", 9))
      self.error_password.place(x = 30, y = 160, height = 15)
    else:
#       self.login_user.append(nick)
      self.root.destroy()
      x= Gui(nick)
      x.start()

  def create(self):
    self.nickname = Tkinter.Label(self.root, text = "Get nickname", font = 14)
    self.nickname_1 = Tkinter.Entry(self.root, width = 20,font = 2)
    self.password = Tkinter.Label(self.root, text = "Get password", font = 14)
    self.password_1 = Tkinter.Entry(self.root, width = 20, font = 2)
    self.log_in = Tkinter. Button(self.root, text = 'login')
    self.root.bind('<Return>', self.check)
    self.log_in.bind('<Button-1>', self.check) 
    self.show_login()

  def show_login(self):
    self.nickname.place(x = 30, y = 20, height = 30)
    self.nickname_1.place(x = 20, y = 45, height = 30)
    self.password.place(x = 30, y = 100, height = 30)
    self.password_1.place(x = 20, y = 125, height = 30)
    self.log_in.place(x = 130, y = 160, height = 30, width = 95)
    

  def login(self):
    self.root.mainloop()

class Gui:

  def __init__ (self, nick ):
    self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    self.IP_address = str('127.0.0.1') 
    self.Port = int(10000) 
    self.connection_socket.connect((self.IP_address, self.Port)) 
    self.main = Tkinter.Tk() # tworze pole nadrzedne
    self.main.geometry("600x400") #definiuje wymiary pola nadrzednego
    self.main.resizable(False, False)
#     self.all_users = user_list
    self.all_users = []
    self.nick = nick
    self.main.after(1, self.read_from_server)
    self.main.after(1000, self.ping)
    self.add_widget()


  def ping(self):
    self.connection_socket.send("ping;;%s" %self.nick)
    self.main.after(1000, self.ping)
    

  def read_from_server(self):
    read_sockets, write_socket, error_socket = select.select([self.connection_socket],[],[], 0.1)
    for socks in read_sockets:
      if socks == self.connection_socket:
        message = socks.recv(2048)
        message = message.split(";;")
        if message[0] == "ping":
          self.users(message[1], None)
        elif message[0] == "close":
          self.users(message[1], 1)
        else:
          self.users(message[0], None)
          self.mess1.configure(state = NORMAL)
          self.mess1.insert(Tkinter.END, '%s> %s \n' %(message[0], message[1]))
          self.mess1.see(Tkinter.END)
          self.mess1.configure(state = DISABLED)
    self.main.after(1, self.read_from_server)


  def on_message_send_requested(self, event):
    message = self.text_input.get() # pobiera tekst z okienka write
    self.text_input.delete(0, Tkinter.END)
    self.mess1.tag_config('you', foreground="red")
    if message != '':
      self.mess1.configure(state = NORMAL)
      send_message = "%s;;%s" %(self.nick, message)
      self.connection_socket.send(send_message)
      self.mess1.insert(Tkinter.END, '%s> %s \n' %(self.nick, message), 'you') #wyswietla wprowadzony tekst
      self.mess1.see(Tkinter.END) #pokazuje zawsze najnowszy wpis
      self.mess1.configure(state = DISABLED)

  def users(self, nick, close):
    self.user.configure(state = NORMAL)
    self.user.delete('1.0', Tkinter.END)
    self.user.tag_config('you', foreground="red")
    if self.all_users.count(nick) == 0:
      self.all_users.append(nick)
    if close == 1:
      self.all_users.remove(nick)
    for i in self.all_users:
      if i == self.nick:
        self.user.insert(Tkinter.END, '%s(you) \n' %i, 'you')
      else:
        self.user.insert(Tkinter.END, '%s \n' %i)
    self.user.see(Tkinter.END)
    self.user.configure(state = DISABLED)

  def add_widget(self):
    self.mess1 = Tkinter.Text(self.main, height = 17, width = 30, font = 2, state = DISABLED) #tworzy pole tekstowe w strefie main, state = blokuje wpisywanie w okno
    self.text_input = Tkinter.Entry(self.main, width = 40, font = 2) #tworzy pole dp wprowadzania tekstu w strefie main
    self.send = Tkinter.Button(self.main, text = "send") #tworzy przycisk w strefie main
    self.send.bind('<Button-1>', self.on_message_send_requested) # akcja dla klikniecia przycisku myszki
    self.scroll_1 = Tkinter.Scrollbar(self.main, command = self.mess1.yview) #dodanie scrolla 
    self.mess1.configure(yscrollcommand = self.scroll_1.set) #config scroll
    self.user = Tkinter.Text(self.main, height = 10, width = 20, font = 2, state = DISABLED)
    self.scroll_2 = Tkinter.Scrollbar(self.main, command = self.user.yview)
    self.user.configure(yscrollcommand = self.scroll_2.set)
    self.label = Tkinter.Label(self.main, text = 'Users', font = ("Helvetica", 16))
    self.main.bind('<Return>', self.on_message_send_requested)
    self.show() #wywolanie funkcji

  def show(self):
    self.text_input.place(x = 50, y = 350, height = 30) #definicje css
    self.mess1.place(x = 15, y = 15)
    self.send.place(x = 455, y=350, height = 30, width = 95 )
    self.scroll_1.place(x = 320, y = 16, height = 327, width = 20 )
    self.user.place(x = 350, y = 100)
    self.scroll_2.place(x = 555, y = 101, height = 194, width = 20 )
    self.label.place(x = 430, y = 70)
    self.users(self.nick, None)


  def on_closing(self):
    self.connection_socket.send("close;;%s" %self.nick)
    self.connection_socket.close()
    self.main.destroy()


  def start(self):
    self.main.protocol("WM_DELETE_WINDOW", self.on_closing)
    self.main.mainloop()



login = Get_in()
login.login()


