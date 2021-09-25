#importing all necessary Sender side support libraries 
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

#function to handle sender operation
def my_sender():
    # selecting the flow control protocol
    print('Input client type-----')
    print('1.Stop and wait\n2.Go back N\n3.Selective repeat\n')
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

        # Loop until client process stops
        while(True):
            #the close option is provided for closing once the operation is done
            print('Input options-----\n1.Send data\n2.Close\n')
            choice=int(input('Enter option : '))

            
            if(choice==1):
                client.send(str.encode("request for sending"))
            elif(choice==2):
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

                    # Enter data file name where data is stored
                    file_name='test.txt'

                    # Receive available receiver list from server
                    receiver_list=data.split('$')

                    # Print the list and choose one of them for data transfer
                    print('Available clients-----')
                    for index in range(0,len(receiver_list)):
                        print((index+1),'. ',receiver_list[index])
                    choice=int(input('\nYour choice : '))
                    choice-=1

                    # Ensure that the choice is valid
                    while(choice not in range(0,(len(receiver_list)))):
                        choice=int(input('Correctly input your choice : '))
                        choice-=1

                    # Notify server about the choice
                    s.send(str.encode(str(choice)))

                    # Get receiver port from server
                    receiverAddress = int(s.recv(1024).decode())

                    # Initialize sender object
                    my_sender=senderList[fcpType].Sender(client,name,senderAddress,receiver_list[index],receiverAddress,file_name)
                    
                    # Start transmission (using sender object)
                    my_sender.transmit()

                    # Get and print notification from server about data transfer complition
                    data=s.recv(1024)
                    data=data.decode()
                    print(data)

               
            # If no data sent/received for an hour, again ask for user options(loop again)
            if not (readable or writable or exceptionals):
                continue


if __name__=='__main__':
        my_sender()    