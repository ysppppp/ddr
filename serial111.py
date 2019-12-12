import serial
from time import sleep

ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate

#received_data = ser.read()
#print (received_data)
while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    a = received_data.decode("utf-8").split(",")
    if(a[0] == "$GNGGA"):
        print (a)                   #print received data
    ser.write(received_data)                #transmit data serially 