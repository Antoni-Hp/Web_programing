#!/usr/bin/env python
import socket 
import select 
import sys 
from thread import *
#AF_INET - domena adresowa gniazda (socket),  SOCK_STREAM - typ gniazda
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#SOL_SOCKET - warstwa gniazda socket.SO_REUSEADDR - powiazanie z gniazdem, 1 - ilosc prob
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
  
# podaje adres Ip
IP_address = str('127.0.0.1') 
  
# podaje nr portu 
Port = int(10000) 
  
# oczekiwanie na polaczenie
server.bind((IP_address, Port)) 

#slucha 10 aktywnych polaczen  
server.listen(10) 
#lista clients
list_of_clients = [] 
  
def clientthread(conn, addr): 
  
    # wysylanie wiadomosci po dolaczeniu do chatu 
#     conn.send("Welcome to this chatroom!") 
  
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
                    # wywoluje funcje transmisji by wyslac do wszystkich 
                    message_to_send = message 
                    broadcast(message_to_send, conn) 
  
                else: 
                    remove(conn) 
  
            except: 
                continue
  
#wyslanie do wszystkich poza osoba wysylajaca"
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
  
                # if the link is broken, we remove the client 
                remove(clients) 
  
#usuniecie klientow z listy
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  
    #akceptuje polaczenie i przechowuje adres oraz typ gniazda
    conn, addr = server.accept() 
  
    # dodaje do listy klientow
    list_of_clients.append(conn) 
  
    # wypisuje klientow ktorzy sie polaczyli 
    print addr[0] + " connected"
  
    #tworzy osobny watek dla kazdego klienta
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 