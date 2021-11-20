import socket      
import os 


#AF_INET used for IPv4
#SOCK_DGRAM used for UDP protocol
s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
#binding IP and port 


available_ip_queue = []
available_ip_queue.append('0.0.0.0')
available_ip_queue.append('0.0.0.1')

connected_clients = []
s.bind(('127.0.0.1',12345))

print("Server started ...")
print("Waiting for Client response...") 
#recieving data from client


#dictionary to handle all the clients 
clients_pid_to_ip = {}
clients_addr_to_pid = {}
import errno
import os


def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


while True:
    dormant_clients = []
    data, addr = s.recvfrom(1024)
    
    for key, value in clients_addr_to_pid.items():
        if check_pid(value) == False:
            dormant_clients.append(value)
    #print (dormant_clients)
    for client_pid in dormant_clients:
        #print (str(client_pid) + ' freed')
        available_ip_queue.append(clients_pid_to_ip[client_pid])
        #del clients_pid_to_ip[client_pid]

    
    if addr in clients_addr_to_pid.keys():
        print ( data.decode() + " sent to server by ip :- " + clients_pid_to_ip[clients_addr_to_pid[addr]])
    else:
        if len(available_ip_queue) == 0: 
            msg = "Sorry ip address cannot be assigned !"
            s.sendto(msg.encode('utf'), addr)
        else:
            #print ("toubleshoot :- " + data.decode()) 
            m = available_ip_queue[0]
            client_pid = int(data.decode())
            clients_addr_to_pid[addr] = client_pid
            clients_pid_to_ip[client_pid] = available_ip_queue[0]
            available_ip_queue.pop(0)
            res = s.sendto (m.encode('utf-8'), addr)



       
