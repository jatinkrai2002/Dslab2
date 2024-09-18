# lab 2
# Process client: As ac client to call methods for This interface defines methods for processes to interact with the BSS protocol. 
# Name: Jatin K rai
#DawID

import Pyro5.api

# Process Logic:
# Each process creates its own Process object and references a shared BSSManager object.
# Processes use send to send messages. This triggers updates to the local vector clock and sends the
# message with the clock to the BSSManager.
# The BSSManager maintains a waiting queue for messages and a current token holder.
# When a process receives the token (implicitly or explicitly), it dequeues messages from the waiting queue
# based on their vector clocks (ensuring causal ordering).
# The BSSManager uses RMI to deliver causally ordered messages to the deliver method of the
#corresponding Process objects

try:
    uri = input("Enter the UnicastRemoteObject for BSS Protocol URI: ")
    remote_process = Pyro5.api.Proxy(uri)
except Exception as error:
        print("Pyro5.api.Proxy(): ClockArry Pyro5.api.Proxy failed while calling")
        print (error)
finally:
        print("Pyro5.api.Proxy(): ClockArry Pyro5.api.Proxy completed successfully while calling.")

try:        
    while True:
        print("1. Broadcast message : ")
        print("2. Get Token : ")
        print("3. Deliver : ")
        print("4. Close : ")
        choice = input("Choose an option: ")

        if choice == '1':
            try:
                print("Please provide message in the format of Proces + sequence number + vectore clock")
                localmessage = input ("Message should be in format P1(1,0,0) or P2 (0,1,0) or P3)(0,0,1) : ")
                CSValue, holdinglist = remote_process.send(localmessage)
            except Exception as error:
                print("remote_process.send():  failed.")
                print (error)
            finally:
                print("remote_process.send(): completed successfully.")
            
            print("remote_process.send(): send return value:", CSValue)
            print ("List of process recived :")
            
            for holdingprocess in holdinglist:
                print(holdingprocess)

        elif choice == '2':
            try:
                print("Please provide empty message to get the Token: ")
                CSValue = remote_process.getToken()
            except Exception as error:
                print("remote_process.getToken():  failed.")
                print (error)
            finally:
                print("remote_process.getToken(): completed successfully.")
            
            print("remote_process.getToken(): getToken Value:", CSValue)

        elif choice == '3':
            try:
                print("Please provide message in the format of Proces + sequence number + vectore clock")
                localmessage = input ("Message should be in format P1(1,0,0) or P2 (0,1,0) or P3)(0,0,1) :  ")
                CSValue, deliverlist = remote_process.deliver(localmessage)
            except Exception as error:
                print("remote_process.deliver():  failed.")
                print (error)
            finally:
                print("remote_process.deliver(): completed successfully.")
            
            print("remote_process.deliver(): Sequence Number:", CSValue)
            for deliveringprocess in deliverlist:
                print(deliveringprocess)            

        elif choice == '4':
            print ("Thanks for the closing application")
            break
except Exception as error:
        print("remote_process. Client call process failed.")
        print (error)
finally:
            print("remote_process.Client call process completed successfully.")
