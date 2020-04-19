import DRR
import time
import board
import busio
from threading import Thread, Event, Lock
from queue import Queue
i2c = DRR.busio.I2C(DRR.board.SCL, DRR.board.SDA)

#Setup
TRIG = 22
ECHO = 23
HUMANTEMP = 32
TEMPCOUNT = 0

t_cam = DRR.Thermal_Cam(i2c)
gps = DRR.GPS()
temp_imu = DRR.Sensor(i2c)
gyro_sensor = DRR.Sensor(i2c)

gps_q = Queue()
temp_q = Queue()
gyro_q = Queue()

human_detected = Event()

i2c_lock = Lock()
gps_l = Lock()
temp_l = Lock()
gyro_l = Lock()

#Termal Camera
def detectHuman(DRR.Thermal_cam t_cam):
    while True:
        temp_pixels = t_cam.readVal()
        temp_reading = [temp for layer in temp_pixels for temp in layer]
        for temp in temp_reading:
            if temp >= HUMANTEMP:
                TEMPCOUNT++
        if (TEMPCOUNT > 32):
            human_detected.set()
        # time.sleep(3)
            # return True
        # else:
            # return False
    return

def alertUser():
    while True:
        human_detected.wait()
        print("Human detected!!")
        human_detected.clear()
    return


#GPS
def currentLocation(DRR.GPS gps):
    while True:
        gps_dict = gps.readVal()
        time.sleep(1)
        gps_q.put_nowait(gps_dict)
    return

def printLocation():
    while True:
        if(len(gps_q)!=0):
            curr_loc = gps_q.get_nowait()
            print("Current location: ",curr_loc)
        time.sleep(1.5)
    return

#Temperature
def currentTemp(DRR.Sensor(i2c) temp_imu):
    while True:
        temp_val = temp_imu.read_TEMP()
        time.sleep(1)
        temp_q.put_nowait(temp_val)
    return

def printTemp():
    while True:
        if(len(temp_q)!=0):
            curr_temp = temp_q.get_nowait()
            print("Current temperature: ",curr_temp)
        time.sleep(1.5)
    return

#IMU (Accelerometer, gyro)
def currentGyro(DRR.Sensor(i2c) gyro_sensor):
    while True:
        mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z = gyro_sensor.read_IMU()
        gyro_data = {"gyro x":gyro_x, "gyro y":gyro_y, "gyro z":gyro_z}
        time.sleep(1)
        gyro_q.put_nowait(gyro_data)
    return

def printGyro():
    while True:
        if(len(gyro_q)!=0):
            curr_gyro = gyro_q.get_nowait()
            print("Current gyro: ",curr_gyro)
        time.sleep(1.5)
    return

#Proximity Sensor

#Movement


#Threads
tcam_thread = Thread(target=detectHuman, args=[t_cam])
t_cam_thread.start()
alert_user_thread = Thread(target=alertUser,args=[])
alert_user_thread.start()

gps_thread = Thread(target=currentLocation, args=[gps])
gps_tread.start()
print_gps = Thread(target=printLocation, args=[])
print_gps.start()

temp_thread = Thread(target=currentTemp, args=[temp_imu])
temp_thread.start()
print_temp = Thread(target=printTemp, args=[])
print_temp.start()

gyro_thread = Thread(target=currentGyro, args=[gyro_sensor])
gyro_thread.start()
print_gyro = Thread(target=printGyro, args=[])
print_gyro.start()

t_cam_thread.join()
alert_user_thread.join()
gps_thread.join()
print_gps.join()
temp_thread.join()
print_temp.join()
gyro_thread.join()
print_gyro.join()


#notes:
#Require locks for the Queues
#Need to impliment a loop for the gps_readVal funciton in DRR.py
