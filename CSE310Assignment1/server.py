#!/usr/bin/env python3

import socket

def encodeM(message):
    length = len(message)
    Emessage = "R,"+str(length)+','+message
    #turn string into byte
    Emessage = str.encode(Emessage)
    return Emessage

def decodeM(message):
    message = message.decode()
    parse = message.split(',')
    Tcheck = parse[0]
    Lcheck = parse[1]
    Lcheck = int(Lcheck)
    if Tcheck != 'Q':
        print("Corrupted data")
        Terror = "ErrorT"
        return Terror
    if Lcheck > 255:
        print("Overflow Error: Message is too big")
        Lerror = "ErrorL"
        return Lerror
    Mcheck = parse[2]
    return Mcheck

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
EmailR = False

#creates socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #associate socket with following info
    s.bind((HOST, PORT))
    #enable connections
    s.listen()
    #binds connections togtether
    while True:    
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                #error check below
                #
                #
                if len(data)>0:                
                    email = decodeM(data)
                    if email == 'ErrorT':
                        conn.sendall(encodeM('Corrupted data'))
                    if email == 'ErrorL':
                        conn.sendall(encodeM('Overflow Error: Message is too big'))
                    else:
                        database = open("database.txt", "r")
                        for line in database:
                            #print(line)
                            lineA = line.split(':')
                            if email == lineA[0]:
                                EmailR = True
                                #print('Found')found item
                                messageF = lineA[1]
                                conn.sendall(encodeM(messageF))
                if not data:
                    conn.sendall(encodeM("not found"))
                    break
