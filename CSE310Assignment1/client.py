#!/usr/bin/env python3

import socket
import re

def isValidEmail(email):
    if len(email) > 7:
        if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            return True
        return False

def encode(Type, email):
    length = len(email)
    message = Type+','+str(length)+','+email
    #turn string into byte
    Emessage = str.encode(message)
    return Emessage

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
message = ''
Type = 'Q'
#email = "jane.doe@gmail.com"
email = input("Enter email address:")  # Python 3
while isValidEmail(email) != True:
    print("This is not a valid email address try again")
    email = input("Enter email address:")


message = encode(Type, email)
#length = len(email)
#message = Type+','+str(length)+','+email
#turn string into byte
#Emessage = str.encode(message)
#print(message)
#print(Emessage.decode())
if len(message) < 257:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message)
        data = s.recv(1024)
        #s.close()    
    print(data)
    answer = data.decode()
    parse = answer.split(',')
    Tcheck = parse[0]
    Lcheck = parse[1]
    Lcheck = int(Lcheck)
    Mcheck = parse[2]
    if Tcheck != "R":
        print("Type Check Error:Message is corrupted")
    if Lcheck > 255:
        print("Overflow Error: Message is too big")   
    if Tcheck == "R":
        if Lcheck < 255:
            print('The owner of the email is:',Mcheck )
else:
    print("Overflow Error: Message is too big")
