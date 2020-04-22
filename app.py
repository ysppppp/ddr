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
OBSTACLE = 15

motorL = DRR.motor(18)
motorR = DRR.motor(13)

t_cam = DRR.Thermal_Cam(i2c)
gps = DRR.GPS()
temp_imu = DRR.Sensor(i2c)
gyro_sensor = DRR.Sensor(i2c)

us_dis = DRR.Ultrasonic(TRIG,ECHO)

#gps_q = Queue()
temp_q = Queue()
gyro_q = Queue()
dis_q = Queue()

human_detected = Event()
obstacle_detected = Event()

def moveL(speed):
    while True:
        motorL.move_forward(speed)

def moveR(speed):
    while True:
        motorR.move_forward(speed)

def movement():
    while True:
        obstacle_detected.wait()
        motorR.stop()
        time.sleep(1)
        obstacle_detected.clear()

moveL_thread = Thread(target=moveL, arg=[20])
moveL_thread.start()
moveR_thread = Thread(target=moveR, arg=[20])
moveR_thread.start()
movemment_thread = Thread(target=movement, arg=[])
movement_thread.start()

moveL_thread.join()
moveR_thread.join()
movement_thread.join()

#i2c_lock = Lock()
#gps_l = Lock()
#temp_l = Lock()
#gyro_l = Lock()
#Ultrasonic Distance Sensor
def detectObstacle(us_dis):
    while True:
        distance = us_dis.distance()
        time.sleep(1)
        dis_q.put(distance)
    return
def obstacleCheck():
    while True:
        dis = dis_q.get()
        if (dis < OBSTACLE):
            obstacle_detected.set()

def obstacleDetected():
    while True:
        obstacle_detected.wait()
        print('too close to an object')
        obstacle_detected.clear()

#Termal Camera
def detectHuman(t_cam):
    while True:
        TEMPCOUNT = 0
        temp_pixels = t_cam.readVal()

        print(temp_pixels)

        temp_reading = [temp for layer in temp_pixels for temp in layer]
        for temp in temp_reading:
            if temp >= HUMANTEMP:
                TEMPCOUNT+=1
        print(TEMPCOUNT)
        if (TEMPCOUNT > 32):
            human_detected.set()
            time.sleep(3)
#            return True
#        else:
#            return False



def alertUser():
    while True:
        human_detected.wait()
        print("Human detected!!")
        human_detected.clear()
    return


#GPS
#def currentLocation(gps):
#    while True:
#        gps_dict = gps.readVal()
#        time.sleep(1)
#        gps_q.put_nowait(gps_dict)
#        print('hi1')
#    return
#
#def printLocation():
#    while True:
#        print('hi2')
#        if(gps_q.empty == False):
#            curr_loc = gps_q.get_nowait()
#            print("Current location: ",curr_loc)
#        time.sleep(1.5)
#    return

#Temperature
def currentTemp(temp_imu):
    while True:

        temp_val = temp_imu.read_TEMP()
#        print(temp_val)
        time.sleep(1)
        temp_q.put(temp_val)
    return

def printTemp():
    while True:
#        print('hi2')
        if(temp_q.qsize()!=0):
            curr_temp = temp_q.get()
            print("Current temperature: ",curr_temp)
        time.sleep(1.5)
    return

#IMU (Accelerometer, gyro)
def currentGyro(gyro_sensor):
    while True:
        mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z = gyro_sensor.read_IMU()
        gyro_data = {"gyro x":gyro_x, "gyro y":gyro_y, "gyro z":gyro_z}
        time.sleep(1)
        gyro_q.put_nowait(gyro_data)
    return

def printGyro():
    while True:
        if(gyro_q.qsize()!=0):
            curr_gyro = gyro_q.get_nowait()
            print("Current gyro: ",curr_gyro)
        time.sleep(1.5)
    return

#Proximity Sensor

#Movement


#Threads
t_cam_thread = Thread(target=detectHuman, args=[t_cam])
t_cam_thread.start()
alert_user_thread = Thread(target=alertUser,args=[])
alert_user_thread.start()

us_dis_thread = Thread(target=detectObstacle, args=[us_dis])
us_dis_thread.start()
obstacleCheck_thread = Thread(target=obstacleCheck)
obstacleCheck_thread.start()
obstacleDetected_thread = Thread(target=obstacleDetected)
obstacleDetected_thread.start()
#gps_thread = Thread(target=currentLocation, args=[gps])
#gps_thread.start()
#print_gps = Thread(target=printLocation, args=[])
#print_gps.start()

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

us_dis_thread.join()
obstacleCheck_thread.join()
obstacleDetected_thread.join()
#gps_thread.join()
#print_gps.join()
temp_thread.join()
print_temp.join()
gyro_thread.join()
print_gyro.join()


#notes:
#Require locks for the Queues
#Need to impliment a loop for the gps_readVal funciton in DRR.py
