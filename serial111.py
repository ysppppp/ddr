import serial
from time import sleep

ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
print('1')
received_data = ser.read()
print (received_data)
#while 1:
#    
#    received_data = ser.read()              #read serial port
#    sleep(0.03)
##    data_left = ser.inWaiting()             #check for remaining byte
##    received_data += ser.read(data_left)
#    print (received_data)                   #print received data
#    print('1')
##    ser.write(received_data)                #transmit data serially 