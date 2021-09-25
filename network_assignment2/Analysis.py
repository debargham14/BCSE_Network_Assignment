# Define bandwidth (in bps)
bandwidth = 4000


# Function to store analysis of transmission into specified file
def storeReport(senderName, receiverName, analysis_file_name, effectivePkt, totalPkt, totalTime, rttStore:list):

    # Open the file
    file=open(analysis_file_name,'a')

    successfullTransmissionTime = (totalTime/effectivePkt)
        
    # Write different parameters of analysis into the file
    file.writelines("\n"+senderName+' is sending data to '+receiverName+"--------------------\n")
    file.writelines('Total packet sent = {}\n'.format(totalPkt))
    file.writelines('Effective packet sent = {}\n'.format(effectivePkt))
    file.writelines('Total time taken = {:6.6f} minutes\n'.format((totalTime/60)))
    throughput = (effectivePkt*72*8)/totalTime
    file.writelines('Receiver Throughput = {:6d} bps\n'.format(int(throughput)))
    efficiency = (throughput/bandwidth)
    file.writelines('Utilization percentage = {:6.2f} %\n'.format((efficiency*100)))
    file.writelines('Average Successful Transmission time of a packet = {:6.6f} seconds/packet\n'.format(successfullTransmissionTime))
    

    file.writelines("\n")

    # Close the file
    file.close()