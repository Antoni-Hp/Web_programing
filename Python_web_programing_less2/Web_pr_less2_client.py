#!/usr/bin/env python

import Tkinter, sys
from Tkconstants import DISABLED, NORMAL

class Get_in:

  def __init__(self):
    self.root = Tkinter.Tk()
    self.root.geometry("250x230")
    self.root.resizable(False, False)
    self.login_user = []
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
      self.login_user.append(nick)
      self.root.destroy()
      x= Gui(self.login_user, nick)
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

  def __init__ (self, user_list, nick):
    self.main = Tkinter.Tk() # tworze pole nadrzedne
    self.main.geometry("600x400") #definiuje wymiary pola nadrzednego
    self.main.resizable(False, False)
    self.all_users = user_list
    self.nick = nick
    self.add_widget()

  def message(self, event):
    mess = self.write.get() # pobiera tekst z okienka write
    if mess != '':
      self.mess1.configure(state = NORMAL)
      self.all_users.append('Adam')
      self.mess1.insert(Tkinter.END, '%s> %s \n' %(self.nick, mess)) #wyswietla wprowadzony tekst
      self.mess1.see(Tkinter.END) #pokazuje zawsze najnowszy wpis
      self.mess1.configure(state = DISABLED)

  def users(self, option):
    self.user.configure(state = NORMAL)
    for i in self.all_users:
      self.user.insert(Tkinter.END, '%s \n' %i)
    self.user.see(Tkinter.END)
    self.user.configure(state = DISABLED)

  def add_widget(self):
    self.mess1 = Tkinter.Text(self.main, height = 17, width = 30, font = 2, state = DISABLED) #tworzy pole tekstowe w strefie main, state = blokuje wpisywanie w okno
    self.write = Tkinter.Entry(self.main, width = 40, font = 2) #tworzy pole dp wprowadzania tekstu w strefie main
    self.send = Tkinter.Button(self.main, text = "send") #tworzy przycisk w strefie main
    self.send.bind('<Button-1>', self.message) # akcja dla klikniecia przycisku myszki
    self.scroll_1 = Tkinter.Scrollbar(self.main, command = self.mess1.yview) #dodanie scrolla 
    self.mess1.configure(yscrollcommand = self.scroll_1.set) #config scroll
    self.user = Tkinter.Text(self.main, height = 10, width = 20, font = 2, state = DISABLED)
    self.scroll_2 = Tkinter.Scrollbar(self.main, command = self.user.yview)
    self.user.configure(yscrollcommand = self.scroll_2.set)
    self.label = Tkinter.Label(self.main, text = 'Users', font = ("Helvetica", 16))
    self.main.bind('<Return>', self.message)
    self.show() #wywolanie funkcji

  def show(self):
    self.write.place(x = 50, y = 350, height = 30) #definicje css
    self.mess1.place(x = 15, y = 15)
    self.send.place(x = 455, y=350, height = 30, width = 95 )
    self.scroll_1.place(x = 320, y = 16, height = 327, width = 20 )
    self.user.place(x = 350, y = 100)
    self.scroll_2.place(x = 555, y = 101, height = 194, width = 20 )
    self.label.place(x = 430, y = 70)
    self.users(1)

  def start(self):
    self.main.mainloop()



login = Get_in()
login.login()


