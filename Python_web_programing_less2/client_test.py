#!/usr/bin/env python
import socket 
import select 
import sys 
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
IP_address = str('127.0.0.1') 
Port = int(10000) 
server.connect((IP_address, Port)) 
  
while True: 
    sasa = raw_input('')
    # maintains a list of possible input streams 
    sockets_list = [sys.stdinhu, server] 
  
    """ There are two possible input situations. Either the 
    user wants to give  manual input to send to other people, 
    or the server is sending a message  to be printed on the 
    screen. Select returns from sockets_list, the stream that 
    is reader for input. So for example, if the server wants 
    to send a message, then the if condition will hold true 
    below.If the user wants to send a message, the else 
    condition will evaluate as true"""
    read_sockets = select.select(sockets_list,[],[]) 
    print sockets_list
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print message 
        else: 
            message = sys.stdin.readline() 
            server.send(message) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message) 
            sys.stdout.flush() 
server.close() 
