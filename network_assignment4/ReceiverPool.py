import Receiver
import threading
import WalshTableGenerator
import Analysis

if __name__ == '__main__':
    totalReceiver = int(input('\nEnter number of receivers : '))
    wTable = WalshTableGenerator.getWalshTable(totalReceiver)
    output_file = input('\nEnter output data file name : ')
    receiverThreadPool = []
    receiverList = []

    for index in range(0,totalReceiver):
        new_receiver = Receiver.Receiver(index,output_file,wTable[index])
        receiverList.append(new_receiver)
        new_receiver_thread = threading.Thread(target=new_receiver.startReceive,args=())
        receiverThreadPool.append(new_receiver_thread)
        new_receiver_thread.start()

    for index in range(0,totalReceiver):
        receiverThreadPool[index].join()

    pktCount = 0
    totalTime = 0
    for index in range(0,totalReceiver):
        pktCount += receiverList[index].report.pktCount
        totalTime += receiverList[index].report.totalTime

    totalTime /= totalReceiver

    finalReport = Analysis.Report(pktCount,totalTime)
    finalReport.storeReport('Analysis.txt',totalReceiver)
