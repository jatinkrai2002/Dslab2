
# lab 2
# Process Interface: This interface defines methods for processes to interact with the BSS protocol. 
# Name: Jatin K rai
#DawID

from collections import deque
from datetime import datetime
from threading import Thread
from time import sleep
from iLab2BSSManager import iLab2BSSManager
from iLab2BSSManager import myLab2BSSManager
from collections import deque

import Pyro5.api
from abc import ABC, abstractmethod
# send(message): Sends a message to other processes.
# deliver(message): Delivers a causally ordered message to the application layer.
# getToken(): Attempts to acquire the BSS token (optional, can be implicit in send
                                                 
# Create a interface 
@Pyro5.api.expose
class iLab2Process(ABC):
    @Pyro5.api.expose
    @abstractmethod
    def send(self, message):
        pass
    	
    @abstractmethod
    @Pyro5.api.expose
    def deliver(self, message):
        pass

    @abstractmethod
    @Pyro5.api.expose
    def getToken(self):
        pass
		
# lab 2
#iLab2Process This class implements the iLab2Process interface. 
# A local queue for holding received messages.
#• A vector clock to track message causality.
#• A reference to a BSSManager object (explained below).
#• It implements methods from the interface:

@Pyro5.api.expose
class myiLab2Process(iLab2Process):
    # assign static
    SequenceNumber = 0
    queueotoholdreceivedmsg = deque()

    def __init__(self):
        self.message = "BSS Broadcast to all process"
        myiLab2Process.queueotoholdreceivedmsg = deque()
        self.localvectorclock = (0,0,0)
        self.BSSManager = myLab2BSSManager()
        self.ProcessNumber = "P" # let us assume process
        myiLab2Process.SequenceNumber = 0
        self.tokenvalue = ""
        self.has_token = 0
        self.hold = 0
        self.BSSManagerMessage = ""



 # send(message): Increments the local vector clock, adds the message with the current clock, and
# calls BSSManager.send(message).

    @Pyro5.api.expose
    def  send(self, message):
        try:
            #assume message is clock type.
            # The message format like Process + Sequencenumber + vectorClock"
            # e.g. P1(1,0,0) or P2(0,1,0) or P3(0,0,1)
            #assume first value is P
            #extract Process id, sequence number extract vector
            self.processId=message[0]
            self.sequenceNumber = message[1]
            lastind = len(message)
            self.localvectorclock= eval(message[2:lastind])
            myiLab2Process.SequenceNumber =  self.sequenceNumber
            self.ProcessNumber = str(self.processId) + ":" + str(self.sequenceNumber)

                        #getToken from BSS Manager with empty message for sending to BSS

            self.tokenvalue = self.getToken()
            self.has_token = 1

            #Check for any message for sending process in the queueotoholdreceivedmsg queue 
            if (len(myiLab2Process.queueotoholdreceivedmsg) > 0):
                for myqueuemessage in myiLab2Process.queueotoholdreceivedmsg:
                    if (str(myqueuemessage).find (str(self.ProcessNumber)) > -1):
                        # first deliver message and then ready for send
                        self.has_token = 1
                        self.tokenvalue = "Temp Token value for " +  str(self.processId) + str(self.sequenceNumber)
                        self.hold = 1
            if (self.has_token == 1 and  self.hold == 1):
                self.deliver (message)
            #Reset Token
            self.has_token = 0
            
            self.BSSManagerMessage, returnholdingQueue  = self.BSSManager.send (message)

            if(len(returnholdingQueue) > 0):
                 for returnprocesidval in returnholdingQueue:
                    myiLab2Process.queueotoholdreceivedmsg.append(returnprocesidval)

             #Print all the message from holding queue.
            for holdingprocess in myiLab2Process.queueotoholdreceivedmsg:
                print (holdingprocess)

            if (self.BSSManagerMessage.lower() == "delivered"):
                    self.has_token = 0
                    self.hold =  0
            elif (self.BSSManagerMessage.lower() == "hold"):
                    self.hold = 1
            else:
                    self.BSSManagerMessage = "Empty"
                    #stay for proces
                
        except Exception as error:
            print("send(): Process Send failed.")
            print (error)
        finally:
            print("send(): Process Send completed successfully.")
        return self.BSSManagerMessage, myiLab2Process.queueotoholdreceivedmsg

# deliver(message): Processes the message based on application logic.
    @Pyro5.api.expose
    def deliver (self, message):
        try:
            # check for message.
            self.BSSManagerMessage = ""
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
            self.ProcessNumber = str(self.processId) + str(self.sequenceNumber)
            
            if (self.has_token== 0 and self.hold == 1):
                #forcefully assigned token for this process to deliver.
                self.has_token = 1
                self.tokenvalue = "Token Value for Process: P" + str( self.ProcessNumber)

            #This is for normal deliver process after token   
            if (self.has_token == 1):
                if (self.tokenvalue.find(self.ProcessNumber) > -1 ):
                    receviedmessagecontainprocess =  deque()
                    #makesure Process delivered value
                    
                    for myprocessIdandSequenceNumber in myiLab2Process.queueotoholdreceivedmsg:
                        print (myprocessIdandSequenceNumber)
                        #for myprocessIdandSequenceNumber in myiLab2Process.queueotoholdreceivedmsg:
                        #check message in the recieving queue
                        if (str(myprocessIdandSequenceNumber).find(self.mssagenumber ) > -1):
                            # remove message from queue and consider to be delivered
                            receviedmessagecontainprocess.append (myprocessIdandSequenceNumber)
                            print("Delivered message from receving end to correspondig process" + str(myprocessIdandSequenceNumber))
                        elif (str (myprocessIdandSequenceNumber).find (str(self.processId) + ":" +str(self.sequenceNumber)) > -1) :
                            receviedmessagecontainprocess.append (myprocessIdandSequenceNumber)
                            print("Delivered message from receving end to correspondig process" + str(myprocessIdandSequenceNumber))             
                    
                    for removedmessage in receviedmessagecontainprocess:
                        if removedmessage in myiLab2Process.queueotoholdreceivedmsg:
                            myiLab2Process.queueotoholdreceivedmsg.remove(removedmessage)
                            print("Removed message from received holding queue end " + str( myprocessIdandSequenceNumber))
                            
                    if (len(myiLab2Process.queueotoholdreceivedmsg)) > 0:
                        print ("Reivng Queue has messages :")
                        self.hold = 1
                    else:
                        print ("Reivng Queue has zero messages (it is empty):")
                        self.hold = 0

            #Make sure token and process id is not in the queue.
            self.has_token  = 0
            self.tokenvalue = ""

            if (self.hold == 1):
              #Print all the message from holding queue.
                for holdingprocess in myiLab2Process.queueotoholdreceivedmsg:
                    print (holdingprocess)

            if (self.hold == 0 and  self.has_token == 0):
                #call release token and resent process,
                self.BSSManagerMessage = self.BSSManager.releaseToken()

        except Exception as error:
            print("deliver (): Process deliver failed.")
            print (error)
        finally:
            print("deliver(): Process deliver completed successfully.")
        
        return self.BSSManagerMessage, myiLab2Process.queueotoholdreceivedmsg
    
# getToken (optional): Implements logic to acquire the token from BSSManager (e.g., using RMI calls)
    @Pyro5.api.expose
    def getToken(self):
        try: 
            # if message is empty then BSSManager.send method will return Token Value
            self.BSSManagerMessage = self.BSSManager.send ("")

        except Exception as error:
            print("getToken(): Process getToken failed.")
            print (error)
        finally:
            print("getToken(): Process getToken completed successfully.")
        return self.BSSManagerMessage
    
        
#Test code for Process
#testmyiLab2Process = myiLab2Process()
#print(testmyiLab2Process.send("P1(1,0,0)"))
#print(testmyiLab2Process.getToken())
#print(testmyiLab2Process.deliver("P1(1,0,0)"))

#Act as Server.
try:
    #make it server ready for remote process.
    daemon = Pyro5.api.Daemon()
except Exception as error:
    print("rPyro5.api.Daemo(): failed.")
    print(error)
finally:
    print("Pyro5.api.Daemo(): completed successfully.")

try:
    #make it server ready for remote process.
    uri = daemon.register(myiLab2Process)
except Exception as error:
    print("Pyro5.api.Daemo.register(): failed.")
    print(error)
finally:
    print("Pyro5.api.Daemo.register() : completed successfully.")

try:
    #make it server ready for remote process.
    print("UnicastRemoteObject for BSS Protocol=")
    print("Ready. UnicastRemoteObject URI=", uri)
    daemon.requestLoop()
except Exception as error:
    print("Pyro5.api.Daemo.requestLoop(): failed.")
    print(error)
finally:
    print("Pyro5.api.Daemo.requestLoop() : completed successfully.")


