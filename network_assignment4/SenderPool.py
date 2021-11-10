from threading import Thread
import Sender
import threading
import Analysis
import WalshTableGenerator

if __name__ == '__main__':
    totalSender = int(input('Enter number of sending stations : '))
    wTable = WalshTableGenerator.getWalshTable(totalSender)
    input_file = input('\nEnter input data file name : ')
    senderThreadPool = []
    senderList = []
    for index in range(0,totalSender):
        new_sender = Sender.Sender(index,input_file,wTable[index])
        senderList.append(new_sender)
        new_sender_thread = threading.Thread(target=new_sender.startTransmission,args=())
        senderThreadPool.append(new_sender_thread)
        new_sender_thread.start()

    for index in range(0,totalSender):
        senderThreadPool[index].join()

    pktCount = 0
    totalTime = 0
    for index in range(0,totalSender):
        pktCount += senderList[index].report.pktCount
        totalTime += senderList[index].report.totalTime

    totalTime /= totalSender

    finalReport = Analysis.Report(pktCount,totalTime)
    #finalReport.storeReport('Analysis2.txt',totalSender)