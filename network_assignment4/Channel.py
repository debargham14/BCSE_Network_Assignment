import socket
import pickle
import threading
import time
import WalshTableGenerator

# Define time-slot
timeSlot = 0.05

# Initialize store for receiving sender data
senderDataStore = []

# Initialize store for flags if sender sent data or not
senderDataFlag = []

# Initialize total number of senders / receivers
totalSender = 0

# Initialize walsh code length
walshCodeLength = 0

# Initialize store to save receiver connections
receiverList = []

# Initialize array to indicate valid receiver
validReceiver = []

# Initialize variable to denote end of transmission
endTransmission = False

# Function to add the individual codes and send them to each receiver
def manageData():
    global totalSender, walshCodeLength, senderDataStore, senderDataFlag, receiverList, endTransmission, validReceiver

    # loop until transmission ends
    while not endTransmission:
        # Wait for a time-slot
        time.sleep(timeSlot)

        # Initialize data to be sent
        dataToSend = [0 for i in range(0,walshCodeLength)]

        flag = False
        flag2 = False

        # Loop to get next coded data sent by each sender and add them with final one
        for index in range(0,totalSender):
            if senderDataFlag[index]:
                senderData = senderDataStore[index].pop(0)
                for j in range(0,walshCodeLength):
                    dataToSend[j] += senderData[j]
                if len(senderDataStore[index]) == 0:
                    senderDataFlag[index] = False
                flag = True
                flag2 = True
        
       
        # Send final data to each receiver
        for index in range(0,len(receiverList)):
            if flag:
                # Print summed-up data to be sent
                print('Channel is sending data : ',dataToSend)
                flag = False

            if validReceiver[index] and flag2:
                receiverList[index].send(pickle.dumps(dataToSend))


# Function for run method of client thread
def sender(connection):
    global senderDataFlag
    global senderDataStore
    global totalSender
    global receiverList
    global validReceiver

    # Get sender number from sender
    connection.send(str.encode("Sender number"))
    senderNumber = int(connection.recv(1024).decode())
    connection.send(str.encode("Okay"))

    # Print sender connection information
    print('Sender {:d} connected with channel'.format(senderNumber))

    # Wait and receive sender sent data
    data = pickle.loads(connection.recv(1024))

    # Loop until data transmission ends
    while data!="end":
        
        # Append data into sender data list
        senderDataStore[senderNumber].append(data)

        # Make sender sent data flag true
        senderDataFlag[senderNumber] = True

        # Wait for next data
        data = pickle.loads(connection.recv(1024))

        # If data transmission ends, notify receiver
        if data == 'end':
            print('Sender number = ',senderNumber)
            
    while senderDataFlag[senderNumber]:
        time.sleep(0.05)

    time.sleep(0.1)

    # Close the connection and notify corresponding receiver
    connection.close()
    validReceiver[senderNumber] = False
    receiverList[senderNumber].send(pickle.dumps(data))



# Function to specify server functionality
def server(numberOfSenders:int, WalshCodeLength:int):
    global totalSender
    global walshCodeLength
    global endTransmission
    global senderDataFlag
    global senderDataStore
    global receiverList
    global validReceiver
    
    # Set variables
    totalSender = numberOfSenders
    walshCodeLength = WalshCodeLength

    senderDataStore = [[] for i in range(0,totalSender)]
    senderDataFlag = [False for i in range(0,totalSender)] 
    validReceiver = [False for i in range(0,totalSender)] 
    senderThreadPool = []

    # Defien server IP address
    server_ip='127.0.0.4'
    # Define server port address
    server_port=1236
    # Define total server address
    server_address=(server_ip,server_port)

    # Initialize server
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Bind server to the address
    server.bind(server_address)

    # Define maximum waiting client requests
    server.listen(5)

    # Notify that server started
    print("Server started")

    # Initialize and start data management thread
    managingThread = threading.Thread(target=manageData,args=())
    managingThread.start()

    count = 0

    # Put server on listen mode and accept client requests
    while count<(2*totalSender):
        # Accept client request
        new_connection,address=server.accept()

        # Receive client name (sender/receiver)
        name=new_connection.recv(1024)
        name=name.decode()

        # Update sender and receiver list 
        # If it's receiver add receiver connection and address into list
        if name == 'receiver':
            receiverList.append(new_connection)
            print('Receiver {:d} connected with channel'.format(count))
            validReceiver[count] = True

        # If it's sender add sender conection into list
        # Send corresponding receiver address to sender
        # Start sender thread providing the receiver connection
        elif name == 'sender':
            # Define and start new client thread
            new_thread=threading.Thread(target=sender,args=(new_connection,))
            senderThreadPool.append(new_thread)
            new_thread.start()

        count += 1

    for index in range(0,totalSender):
        senderThreadPool[index].join()
    
    # End the transmission
    endTransmission = True
    managingThread.join()

    for receiver_connection in receiverList:
        receiver_connection.close()

    # Close server
    server.close()


# Main function
if __name__=='__main__':
    numberOfSenders = int(input('Enter number of sending stations : '))
    num = WalshTableGenerator.getNextPowerof2(numberOfSenders)
    server(numberOfSenders,num)