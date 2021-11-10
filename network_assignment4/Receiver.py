import socket
import pickle
import time
import Analysis

# Define Receiver class to handle data receiving 
class Receiver:
    # Function to initialize obect
    def __init__(self, receiverNo:int, file:str, WalshCode):
        # Get the client/receiver connection and other informations (name, data file name)
        self.connection         = 0
        self.file_name          = file
        self.receiverNo         = receiverNo
        self.walshCode          = WalshCode
        self.report             = Analysis.Report(0,0)
        self.pktCount           = 0
        self.startTime          = 0

    # Function to get character from 8-bit data
    def getCharacter(self, data):
        string = ''.join(data)
        character = chr(int(string,2))
        return character


    # Function for receiving data
    def receive(self):

        # Wait for data and receive
        data = pickle.loads(self.connection.recv(1024))
        self.startTime = time.time()

        wholeData = ''
        totalData = []
        while data!='end':
            # Print received data
            print('Receiver ',self.receiverNo,' received data : ',data)

            # extract data
            summation = 0
            for i in range(len(data)):
                summation += data[i] * self.walshCode[i]
            
            # extract databit
            summation /= len(self.walshCode)

            # Print coded data to be sent
            print('Receiver ',self.receiverNo,' received data-bit : ',summation,' using Walsh code : ',self.walshCode)

            if summation == 1:
                bit = 1
            elif summation == -1:
                bit = 0
            else: bit = -1

            self.pktCount += 1

            if bit != -1:
                # append the bit to build the character  
                totalData.append(str(bit))

            if len(totalData) == 8:
                character = self.getCharacter(totalData)
                # Print received character
                print('Receiver ',self.receiverNo,' received character : ',character)
                wholeData += character
                totalData = []

             # Wait for data and receive
            data = pickle.loads(self.connection.recv(1024))

        if wholeData != '':
            # print(total_data)
            file = open(self.file_name,'a')
            file.write(wholeData)
            file.write('\n')
            file.close()


    # Function to connect receiver with channel and start receiving
    def startReceive(self):

        # Initialize the socket
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # Connect with the channel
        channel_ip = '127.0.0.4'
        channel_port = 1236
        channel_address = (channel_ip,channel_port)
        self.connection.connect(channel_address)

        # Notify channel that it's a sender
        self.connection.send(str.encode('receiver'))

        # Start receiving
        self.receive()

        # Close the connection
        self.connection.close()

        endTime = time.time()
        totalTime = (endTime - self.startTime)
        self.report = Analysis.Report(self.pktCount,totalTime)