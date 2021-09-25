# import socket module
import socket
import crc			
import error
import checksum
import lrc

import matplotlib.pyplot as plt
import numpy as np


SERVER = "127.0.0.1"        # host interface of the server
PORT = 12345                # port on which the server listens

# create a new socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # connect to server
    client.connect((SERVER, PORT))
        # recieve data from server
   
    flag = False
    msg_array = []
    with open ("test.txt", "r") as file:
        data = file.readlines ()
        for line in data:
            msg_array.append(str(line))
    count_crc, count_lrc, count_vrc, count_checksum = 0,0,0,0
    error_caught_by_checksum = []
    error_caught_by_checksum_tainted = []
    
    error_not_caught_by_checksum = []
    error_not_caught_by_checksum_tainted = []

    error_caught_by_crc = []
    error_caught_by_crc_tainted = []

    error_not_caught_by_crc = []
    error_not_caught_by_crc_tainted = []

    error_caught_by_lrc = []
    error_caught_by_lrc_tainted = []

    error_not_caught_by_lrc = []
    error_not_caught_by_lrc_tainted = []

    error_caught_by_vrc = []
    error_caught_by_vrc_tainted = []

    error_not_caught_by_vrc = []
    error_not_caught_by_vrc_tainted = []

    error_caught_by_all_four = []
    error_caught_by_all_four_tainted = []

    error_caught_by_checksum_not_by_crc = []
    error_caught_by_checksum_not_by_crc_tainted = []

    error_caught_by_vrc_not_by_crc = []
    error_caught_by_vrc_not_by_crc_tainted = []
    for i in range (len(msg_array)):
            # take message from user
             # recieve data from server
            
        msg = msg_array[i]
        if msg == "bye":
            client.sendall(bytes(msg, 'UTF-8'))
            break
        #generate the code word for crc
        codeword_crc = crc.CRC.encodeData(msg, "111010101")

        #inject error
        error_codeword_crc = error.InjectError.multipleError (codeword_crc)

        #codeword for checksum
        codeword_checksum = checksum.CHECKSUM.findCheckSum(msg, 4)

        #codeword for LRC
        codeword_lrc = lrc.LRC_VRC.calcLRC(msg)
        
        #error codeword for LRC
        error_codeword_lrc = error.InjectError.burstError(codeword_lrc)
        #inject error
        error_codeword_checksum = error.InjectError.multipleError(codeword_checksum)
        
        #codeword for vrc
        codeword_vrc = lrc.LRC_VRC.calcVRC(msg)
        final_information = error_codeword_checksum + ' ' +  error_codeword_crc + ' ' + error_codeword_lrc + ' ' + codeword_vrc
        final_information1 = error_codeword_crc[:32]
        in_data = client.recv(1024)
        
        print (in_data.decode())
        result = in_data.decode()

        if(result[0] == '1'):
            count_checksum = count_checksum + 1
            error_caught_by_checksum.append (msg)
            error_caught_by_checksum_tainted.append (final_information1)
        else:
            error_not_caught_by_checksum.append(msg)
            error_not_caught_by_checksum_tainted.append(final_information1)
        if(result[1] == '1'):
            count_crc = count_crc + 1
            error_caught_by_crc.append (msg)
            error_caught_by_crc_tainted.append (final_information1)
        else:
            error_not_caught_by_crc.append(msg)
            error_not_caught_by_crc_tainted.append(final_information1)

        if(result[2] == '1'):
            count_lrc = count_lrc + 1
            error_caught_by_lrc.append (msg)
            error_caught_by_lrc_tainted.append (final_information1)
        else:
            error_not_caught_by_lrc.append(msg)
            error_not_caught_by_lrc_tainted.append(final_information1)
        if (result[3] == '1'):
            count_vrc = count_vrc + 1
            error_caught_by_vrc.append (msg)
            error_caught_by_vrc_tainted.append (final_information1)
        else:
            error_not_caught_by_vrc.append (msg)
            error_not_caught_by_vrc_tainted.append (final_information1)
        if (result[0] == '1' and result[1] == '1' and result[2] == '1' and result[3] == '1'):
            error_caught_by_all_four.append(msg)
            error_caught_by_all_four_tainted.append(final_information1)

        if (result[0] == '1' and result[1] == 0):
            error_caught_by_checksum_not_by_crc.append(msg)
            error_caught_by_checksum_not_by_crc_tainted.append(final_information1)
        if(result[3] == '1' and result[1] == 0):
            error_caught_by_vrc_not_by_crc.append(msg)
            error_caught_by_checksum_not_by_crc_tainted.append(final_information1)
        client.sendall (bytes(final_information,'UTF-8'))
    in_data = client.recv(1024)
    print (in_data.decode())
    print ("error detected by checksum : ", (count_checksum * 100) / 131072)
    print ("error detected by crc : ", (count_crc * 100) / 131072)
    print ("error detected by lrc : ", (count_lrc * 100) / 131072)
    print ("error detected by vrc : ", (count_vrc * 100) / 131072)

    count_checksum = (count_checksum * 100) / len(msg_array)
    count_crc = (count_crc * 100) / len (msg_array)
    count_vrc = (count_vrc * 100) / len (msg_array)
    count_lrc = (count_lrc * 100) / len (msg_array)
    print ("error caught by checksum: ", error_caught_by_checksum[0])
    print ("error caught by checksum tainted data: ", error_caught_by_checksum_tainted[0])

    print ("error not caught by checksum : ", error_not_caught_by_checksum[0])
    print ("error not caught by checksum tainted data : ", error_not_caught_by_checksum_tainted[0])

    print ("error caught by crc : ", error_caught_by_crc[0])
    print ("error caught by crc tainted data : ", error_caught_by_crc_tainted[0])

    print ("error not caught by crc : ", error_not_caught_by_crc[0])
    print ("error not caught by crc tainted data : ", error_not_caught_by_crc_tainted[0])

    print ("error caught by lrc : ", error_caught_by_lrc[0])
    print ("error caught by lrc tainted data : ", error_caught_by_lrc_tainted[0])

    
    print ("error not caught by lrc : ", error_not_caught_by_lrc[0])
    print ("error not caught by lrc tainted data: ", error_not_caught_by_lrc_tainted[0])

    print ("error caught by vrc : ", error_caught_by_vrc[0])
    print ("error caught by vrc tainted data : ", error_caught_by_vrc_tainted[0])
    
    print ("error not caught by vrc : ", error_not_caught_by_vrc[0])
    print ("error not caught by vrc tainted data : ", error_not_caught_by_vrc_tainted[0])

    print ("error caught by all four schemes : ", error_caught_by_all_four[0])
    print ("error caught by all four schemes tainted data : ", error_caught_by_all_four_tainted[0])
    
    
    if (len(error_caught_by_checksum_not_by_crc) > 0): 
        print ("error caught by checksum and not by crc : ", error_caught_by_checksum_not_by_crc[0])
    if (len(error_caught_by_checksum_not_by_crc_tainted) > 0):
        print ("error caught by checksum and not by crc tainted data : ", error_caught_by_checksum_not_by_crc_tainted[0])
    
    #print ("error caught by vrc and not by crc : ", error_caught_by_vrc_not_by_crc[0])
    #print ("error caught by vrc and not by crc tainted data : ", error_caught_by_vrc_not_by_crc_tainted[0])
    # creating the dataset
    data = {"checksum":count_checksum, "crc":count_crc, "lrc":count_lrc,
            "vrc":count_vrc}
    courses = list(data.keys())
    values = list(data.values())
    
    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(courses, values, color ='maroon',
            width = 0.4)
    plt.axis([0, 4, 0, 120])
    
    plt.xlabel("error detection schemes")
    plt.ylabel("efficiency")
    plt.title("efficiency of different error detection schemes")
    plt.show()