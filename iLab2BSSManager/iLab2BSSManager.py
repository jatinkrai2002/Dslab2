
# lab 2
#BSSManager Interface: This interface manages manages the BSS protocol logic. . 
# Name: Jatin K rai
#DawID

from collections import deque

import Pyro5.api
from collections import defaultdict
from abc import ABC, abstractmethod

@Pyro5.api.expose
# Create a interface ILab2BSSManager
class iLab2BSSManager(ABC):
    @Pyro5.api.expose
    @abstractmethod
    def send(self, message):
        pass

    @Pyro5.api.expose
    @abstractmethod
    def releaseToken(self):
        pass
    
    
    
# lab 2
#BSSManager Implementation: This class implements the BSSManager interface. It maintains: 
##BSSManager Interface: This interface manages the BSS protocol logic. Methods can include:
# send(message): Receives a message from a process and performs BSS protocol actions.
# releaseToken(): Releases the token (optional, can be implicit in send).


@Pyro5.api.expose
class myLab2BSSManager(iLab2BSSManager):
    P1Stagevalue = 0
    P2Stagevalue = 0
    P3Stagevalue = 0
    tokenholderprocessid = 0
    # assign
    def __init__(self):
        
        self.queueotoholdrequest = deque()
        self.DeliveredMessage = "Delivered"
        self.HoldMessage = "Hold"
        self.ReleaseMessage = "RELEASE"
        self.returnMessage = "Empty"
        self.localvectorclock = (0,0,0)
        self.processnumber = [1,2,3]

# BSSManager Implementation: This class implements the BSSManager interface. It maintains:
# The current token holder (process ID).
# A queue for holding messages waiting to be causally ordered.
# It implements methods from the interface:
# send(message): Updates the local vector clock based on the message clock.
# If the process is the token holder, it dequeues messages from the queue in causal order
#(based on vector clocks) and delivers them to their respective processes using RMI calls
# to deliver.
# If the process is not the token holder, it enqueues the message in the waiting queue.
 

    @Pyro5.api.expose
    def send(self, message):
        try:
            self.queueotoholdrequest.clear()
            if (len(message) < 1):
                # retun token value with round robin
                if (myLab2BSSManager.tokenholderprocessid == myLab2BSSManager.P1Stagevalue):
                    myLab2BSSManager.tokenholderprocessid = 1
                elif (myLab2BSSManager.tokenholderprocessid == myLab2BSSManager.P2Stagevalue):
                    myLab2BSSManager.tokenholderprocessid = 2
                elif (myLab2BSSManager.tokenholderprocessid == myLab2BSSManager.P3Stagevalue):
                    myLab2BSSManager.tokenholderprocessid = 3
                else:
                    #Reset
                    myLab2BSSManager.P1Stagevalue = 0
                    myLab2BSSManager.P2Stagevalue = 0
                    myLab2BSSManager.P3Stagevalue = 0
                    myLab2BSSManager.tokenholderprocessid = 0

                self.returnMessage = "Token Value for Process: P" + str(myLab2BSSManager.tokenholderprocessid)
            else:
                #assume message is clock type.
                # The message format like Process + Sequencenumber + vectorClock"
                # e.g. P1(1,0,0) or P2(0,1,0) or P3(0,0,1)
                #assume first value is P
                #extract Process id, sequence number extract vector
                self.processId=message[0]
                self.sequenceNumber = message[1]
                lastind = len(message)
                self.localvectorclock= eval(message[2:lastind])
                self.mssagenumber = "M" + message[1]

                if (eval(self.sequenceNumber) == 1):
                    myLab2BSSManager.P1Stagevalue += 1
                elif (eval(self.sequenceNumber) == 2):
                    myLab2BSSManager.P2Stagevalue += 1
                elif (eval(self.sequenceNumber) == 3):
                    myLab2BSSManager.P3Stagevalue += 2

                #broadcast message to all processes.
                processIdandSequenceNumber = str(self.processId) + (":") + str (self.sequenceNumber)


                # Broadcast message to all process except own process and increase vector clock
                #assume P1 is the input. so sequence id is 1 and vector clock is (1,0,0)
                for myprocesssequenceid in self.processnumber:
                   if (myprocesssequenceid != eval(self.sequenceNumber)):
                       myprocessIdandSequenceNumber = str(self.processId) + (":") + str (myprocesssequenceid) + ":" + self.mssagenumber + ":"  + str( self.localvectorclock)
                       self.queueotoholdrequest.append(myprocessIdandSequenceNumber)
                       self.tokenholderprocessid = self.sequenceNumber
                    #else do nothing for same process

                print("all the message from holding queue.")
                for holdingprocess in self.queueotoholdrequest:
                    print (holdingprocess)
                
                self.returnMessage = self.HoldMessage
            
                #Process2 and process 3 will be populated in the queue.
        except Exception as error:
            print("requestEntry(): failed.")
            print(error)
        finally:
            print("requestEntry(): completed successfully.")
        
        return self.returnMessage, self.queueotoholdrequest
         
	
# releaseToken (optional): Updates the token holder based on a pre-defined order (e.g., round-robin)
    @Pyro5.api.expose
    def releaseToken(self):
        try:
            #need to be call after send.
            if (myLab2BSSManager.tokenholderprocessid == myLab2BSSManager.P1Stagevalue):
                myLab2BSSManager.tokenholderprocessid = 0
            elif (myLab2BSSManager.tokenholderprocessid == myLab2BSSManager.P2Stagevalue):
                myLab2BSSManager.tokenholderprocessid = 0
            elif (myLab2BSSManager.tokenholderprocessid == myLab2BSSManager.P3Stagevalue):
                myLab2BSSManager.tokenholderprocessid = 0
            else:
                #Reset
                myLab2BSSManager.P1Stagevalue = 0
                myLab2BSSManager.P2Stagevalue = 0
                myLab2BSSManager.P3StageValue = 0
                myLab2BSSManager.tokenholderprocessid = 0
            #next process
            #relase queue also
            self.queueotoholdrequest.clear()

            self.returnMessage = self.ReleaseMessage
        except Exception as error:
            print("releaseToken(): failed.")
            print(error)
        finally:
            print("releaseToken(): completed successfully.")
        return self.returnMessage
    

#Test code for Token Manager
#testmyLab2BSSManager = myLab2BSSManager()
#print(testmyLab2BSSManager.send("P1(1,0,0)"))
#print(testmyLab2BSSManager.releaseToken())

