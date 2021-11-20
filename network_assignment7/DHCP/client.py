import socket
import os
#client program

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
process_id = str(os.getpid())

print ("Client started with process id :- " + process_id)
count = 0
while True:
       #ip ,port = input("Enter server ip address and port number :\n").split()
       if count == 1:
           m = input ("Enter data to the server :")
           res = s.sendto(m.encode('utf-8'), ('127.0.0.1',12345))
       else:
           res = s.sendto (process_id.encode('utf'), ('127.0.0.1', 12345))
           data, addr = s.recvfrom(1024)
           print ('Your assigned ip is :- ' + data.decode())
           count = 1
       
       