import socket      
import os 


#AF_INET used for IPv4
#SOCK_DGRAM used for UDP protocol
s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
#binding IP and port 

print (os.getpid())

available_ip_queue = []
available_ip_queue.append('0.0.0.0')
available_ip_queue.append('0.0.0.1')
available_ip_queue.append('0.0.0.2')

connected_clients = []
s.bind(('127.0.0.1',12345))

print("Server started ...")
print("Waiting for Client response...") 
#recieving data from client


#dictionary to handle all the clients 
clients = {}
import errno
import os

def pid_exists(pid):
    """Check whether pid exists in the current process table.
    UNIX only.
    """
    if pid < 0:
        return False
    if pid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        raise ValueError('invalid PID 0')
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise
    else:
        return True

def find_pid(inode):

    # get a list of all files and directories in /proc
    procFiles = os.listdir("/proc/")

    # remove the pid of the current python process
    procFiles.remove(str(os.getpid()))

    # set up a list object to store valid pids
    pids = []

    for f in procFiles:
        try:
            # convert the filename to an integer and back, saving the result to a list
            integer = int(f)
            pids.append(str(integer))
        except ValueError:
            # if the filename doesn't convert to an integer, it's not a pid, and we don't care about it
            pass
    
    for pid in pids:
        # check the fd directory for socket information
        fds = os.listdir("/proc/%s/fd/" % pid)
        for fd in fds:
            # save the pid for sockets matching our inode
            if ('socket:[%d]' % inode) == os.readlink("/proc/%s/fd/%s" % (pid, fd)):
                return pid
while True:
    data, addr = s.recvfrom(1024)
    dormant_clients = []
    """
    for key, value in clients.items():        
        if pid_exists(key[1]) == False:
            available_ip_queue.append(key[0])
            dormant_clients.append(key[1])
    print (dormant_clients)
    for client in dormant_clients:
        available_ip_queue.append(client)
        clients.pop(client, None)
    """
    if addr in clients.keys():
        s.sendto('acknowledgement msg'.encode(), addr)
        print (str (data.decode()) + ' Received from client with ip :- ' + str(clients[addr]))
    else:
        msg = '' 
        if len(available_ip_queue) == 0: 
            msg = 'Sorry client cannot be provided with ip :- '
        else:
            msg = 'hello new client your assigned ip is :- ' + available_ip_queue[0]
            clients[addr] = available_ip_queue[0]
            available_ip_queue.pop(0)
        s.sendto(msg.encode ('utf-8'), addr)       

       
