from flask import Flask, redirect, render_template
import DRR
import time
import board
import busio
import datetime
import copy
from threading import Thread, Event, Lock
from queue import Queue
i2c = DRR.busio.I2C(DRR.board.SCL, DRR.board.SDA)

#Setup
TRIG = 22
ECHO = 23
HUMANTEMP = 32
OBSTACLE = 15

motorL = DRR.Motor(18)
motorR = DRR.Motor(13)
motorL.move_forward(50)
motorR.move_forward(50)

t_cam = DRR.Thermal_Cam(i2c)
gps = DRR.GPS()
temp_imu = DRR.Sensor(i2c)
gyro_sensor = DRR.Sensor(i2c)
us_dis = DRR.Ultrasonic(TRIG,ECHO)

gps_q = Queue()
temp_q = Queue()
gyro_q = Queue()
dis_q = Queue()

human_detected = Event()
obstacle_detected = Event()

curr_sensor_vals = {"Temperature":None, "Gyro":None,"Current location":None, "Time":None}
human_list = []

start_time = time.time()
curr_time = datetime.datetime.now()
print(curr_time)

def movement():
    while True:
        obstacle_detected.wait()
        motorL.stop()
        print('too close to an object')
        time.sleep(1)
        obstacle_detected.clear()
        motorL.move_forward(50)

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
#Termal Camera
def detectHuman(t_cam):
    startingtime = 0
    while True:
        
        startingtime += 1
        TEMPCOUNT = 0
        temp_pixels = t_cam.readVal()
        # print(temp_pixels)
        temp_reading = [temp for layer in temp_pixels for temp in layer]
        for temp in temp_reading:
            if temp >= HUMANTEMP:
                TEMPCOUNT+=1
        #print(TEMPCOUNT)
        if (TEMPCOUNT > 32):
            print(startingtime)
            if ( startingtime > 15):
                startingtime = 0
                time.sleep(0.5)
                human_detected.set()
                
                
            
        time.sleep(0.5)

def alertUser():
    while True:
        human_detected.wait()
        print("Human detected!!")
        t = copy.copy(currValues())
        human_list.append(t)
        time.sleep(1)
        human_detected.clear()
    return

#def updateHumanList():
#    human_list.append(currValues())

def HumanList():
    return human_list;

#GPS
def currentLocation(gps):
   while True:
       gps_dict = gps.readVal()
       time.sleep(0.5)
       gps_q.put_nowait(gps_dict)
       # print('hi1')
   

# def printLocation():
#    while True
#        if(gps_q.empty == False):
#            curr_loc = gps_q.get_nowait()
#            print("Current location: ",curr_loc)
#        time.sleep(1.5)
#    return

#Temperature
def currentTemp(temp_imu):
    while True:
        temp_val = temp_imu.read_TEMP()
        time.sleep(1)
        temp_q.put(temp_val)
    return

# def printTemp():
#     while True:
        # if(temp_q.qsize()!=0):
        #     curr_temp = temp_q.get()
#             print("Current temperature: ",curr_temp)
#         time.sleep(1.5)
#     return

#IMU (Accelerometer, gyro)
def currentGyro(gyro_sensor):
    while True:
#        print('hello')
        mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z = gyro_sensor.read_IMU()
        gyro_data = {"gyro x":gyro_x, "gyro y":gyro_y, "gyro z":gyro_z}
#        print(gyro_data)
        time.sleep(1)
        
        gyro_q.put(gyro_data)
    

# def printGyro():
#     while True:
#         if(gyro_q.qsize()!=0):
#             curr_gyro = gyro_q.get_nowait()
#             print("Current gyro: ",curr_gyro)
#         time.sleep(1.5)
#     return


def currValues():
    curr_temp = 0
    curr_gyro = {}
    curr_loc = {}
    while True:
        if(gps_q.qsize() != 0):
            curr_loc = gps_q.get_nowait()
            curr_sensor_vals["Current location"] = curr_loc
        if(temp_q.qsize()!=0):
            curr_temp = temp_q.get()
            curr_sensor_vals["Temperature"] = curr_temp
        if(gyro_q.qsize()!=0):
            curr_gyro = gyro_q.get_nowait()
            curr_sensor_vals["Gyro"] = curr_gyro

       
        curr_time = datetime.datetime.now()
        curr_sensor_vals["Time"] = curr_time
        print(curr_sensor_vals["Time"])
        return curr_sensor_vals




app = Flask(__name__, static_folder='')
@app.route("/")
def hello():
    return render_template('home.html')

@app.route('/curdata')
def curData():
    curr_dict = currValues()
    curr_temp = curr_dict["Temperature"]
    curr_gyro = curr_dict["Gyro"]
    curr_loc = curr_dict["Current location"]
    curr_time = curr_dict["Time"]
    
    return render_template('data.html', temp = curr_temp, gyro = curr_gyro, loc = curr_loc, time = curr_time)
#temp = curr_temp, gyro = curr_gyro, loc = curr_loc, time = curr_time
@app.route('/tcam')
def tcam():
    tcampix = t_cam.readVal()
    return render_template("tcam.html", tcam = tcampix)

@app.route('/victims')
def data():
    victimslist = HumanList();
    return render_template("victims.html", victims = victimslist)

if __name__ == "__main__":
    print('Hi')
    #Threads
    t_cam_thread = Thread(target=detectHuman, args=[t_cam])
    t_cam_thread.start()
    alert_user_thread = Thread(target=alertUser,args=[])
    alert_user_thread.start()
    
    us_dis_thread = Thread(target=detectObstacle, args=[us_dis])
    us_dis_thread.start()
    obstacleCheck_thread = Thread(target=obstacleCheck)
    obstacleCheck_thread.start()
    movement_thread = Thread(target=movement, args=[])
    movement_thread.start()
#    us_dis_thread = Thread(target=detectObstacle, args=[us_dis])
#    us_dis_thread.start()
    #obstacleCheck_thread = Thread(target=obstacleCheck)
    #obstacleCheck_thread.start()
    #obstacleDetected_thread = Thread(target=obstacleDetected)
    #obstacleDetected_thread.start()

    gps_thread = Thread(target=currentLocation, args=[gps])
    gps_thread.start()
    #print_gps = Thread(target=printLocation, args=[])
    #print_gps.start()

    temp_thread = Thread(target=currentTemp, args=[temp_imu])
    temp_thread.start()
    # print_temp = Thread(target=printTemp, args=[])
    # print_temp.start()

    gyro_thread = Thread(target=currentGyro, args=[gyro_sensor])
    gyro_thread.start()
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

    t_cam_thread.join()
    alert_user_thread.join()
    us_dis_thread.join()
    obstacleCheck_thread.join()
    obstacleDetected_thread.join()
    gps_thread.join()
    #print_gps.join()
    temp_thread.join()
    # print_temp.join()
    gyro_thread.join()
    # print_gyro.join()
    #print_curr_vals.join()
    us_dis_thread.join()
    obstacleCheck_thread.join()
    movement_thread.join()
