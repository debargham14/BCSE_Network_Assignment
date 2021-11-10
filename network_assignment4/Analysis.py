class Report:
    def __init__(self, pktCount:int, totalTime:float):
        self.pktCount       = pktCount
        self.totalTime      = totalTime

    # Function to store analysis of transmission into specified file
    def storeReport(self, analysis_file_name:str, totalSender:int):

        # Calculate average statistics for each station
        avgPktCount = int(self.pktCount/totalSender)
        avgTotalTime = self.totalTime
        

        # Open the file
        file=open(analysis_file_name,'a')
        
        # Write different parameters of analysis into the file
        file.writelines("\nTest run report with {:d} senders--------------------\n".format(totalSender))
        file.writelines('Total packet sent = {} per sender\n'.format(avgPktCount))
        file.writelines('Total time taken = {:6.6f} seconds\n'.format((avgTotalTime)))
        effectiveBandwidth = (self.pktCount/self.totalTime)
        file.writelines('Effective bandwidth = {:d} bps\n'.format(int(effectiveBandwidth)))
        stt = (self.totalTime/avgPktCount)
        file.writelines('Successful Transmission Time = {:6.6f} seconds per packet\n'.format(stt))
        file.writelines("\n")

        # Close the file
        file.close()