
import serial
import pickle
import time
#from time import sleep

ser = serial.Serial ("/dev/ttyS0", 9600)
sentences = []#Open port with baud rate
current = time.time() # get current time
timeout = 5
endtime = time.time()+timeout 
# endtime = current time + timeout
# modify loop: check if currenttime >= endtime and end it if it is
#for i in range(100):
while current < endtime:
    current = time.time()
    received_data = ser.readline()              
    a = received_data.split(",")
    if a[0] == "$GNGGA":
        gpsData = {
            "ts" : a[1],
            "lat" : a[2]/100.0,
            "latDir" : a[3],
            "long" : a[4]/100.0,
            "longDir" : a[5],
            "fix" : a[6]
        }
    print (gpsData) # was return before
    # sleep(0.03)
    #data_left = ser.inWaiting()             #check for remaining byte
    #received_data += ser.read(data_left)
    #print (received_data)                   #print received data
    #ser.write(received_data)                #transmit data serially
    #print(received_data)
    #print(".............")
    #sentences.append(received_data)
    #return None ////pass

with open("sentences.pkl", 'w') as outfile:
    pickle.dump(sentences, outfile)
