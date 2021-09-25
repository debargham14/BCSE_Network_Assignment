import socket
import select
import SenderSW
import ReceiverSW
import SenderGBN
import ReceiverGBN
import SenderSR
import ReceiverSR

# Build a list to store type of sender or receiver
senderList = [SenderSW,SenderGBN,SenderSR]
receiverList = [ReceiverSW,ReceiverGBN,ReceiverSR]

# Function to handle receiver operation
def my_receiver():
    # Get the flow control protocol
    print('Input client type-----')
    print('1.Stop and wait\n2.Go back N\n2.Selective repeat\n')
    fcpType = int(input('Enter choice = '))
    if(fcpType>3 or fcpType<1):
        fcpType = 1
    fcpType -= 1

    # define server ip address
    SERVER_IP='127.0.0.1'
    # define server port address
    SERVER_PORT=1232

    # start the client socket
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:

        client.connect((SERVER_IP, SERVER_PORT))

        # recieve connection acknowledgement from server
        msg =  client.recv(1024).decode()  
        print("From Server :" , msg, end='')

        # take the client name as input and send it to server
        name=input()

        client.sendall (bytes(name,'UTF-8'))

        # get client port number from server
        address = client.recv(1024).decode()
        
        senderAddress = int(address)

        # Loop until client wants to go offline
        while(True):
            # Enter user's choice and progress accordingly
            # There are 3 choices - send data, just wait(for receiving) and close connection
            print('Input options-----\n1.Receive data\n2.Close\n')
            choice=int(input('Enter option : '))

            # If user wants to send data, request server for that
            # Otherwise just wait
            # if user wants to close, notify server about it and then close
            if(choice!=1):
                client.send(str.encode("close"))
                break

            # Initialize input and output event generators
            inputs=[client]
            output=[]

            # Wait until any input/output event or timeout occurs
            readable,writable,exceptionals=select.select(inputs,output,inputs,3600)
            
            # If input event is generated(any data/signal came from server), handle it
            for s in readable:
                # Receive and decode the data
                data=s.recv(1024).decode()

                # If no other client is connected with server, cancel sending request
                if(data=="No client is available"):
                    print(data)
                    break

                # If this client got sending permission from server
                elif(choice == 1):

                    # Print the receiver starting status
                    print('Receiving data-----')

                    # Input the file name where received data will be stored
                    file_name=''
                    if fcpType == 0: #the selected type is Stop and Wait  
                        file_name='SWARQ_rec.txt'
                    elif fcpType == 1: # the selected type is Go Back N
                        file_name='GBN_rec.txt'
                    else: #the selected type is Selective Repeat 
                        file_name='SR_rec.txt' 

                    # Initialize receiver object
                    receiverAddress = int(data)
                    
                    s.send (bytes("start", 'utf-8'))
                    my_receiver=receiverList[fcpType].Receiver(client,name,senderAddress,receiverAddress,file_name)
                    
                    # Start data receiving through receiver object
                    my_receiver.startReceiving()

               
            
            # If no data sent/received for an hour, again ask for user options(loop again)
            if not (readable or writable or exceptionals):
                continue


if __name__=='__main__':
        my_receiver()    