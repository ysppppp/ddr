import time
import BBIO
import busio
import adafruit_amg88xx
import adafruit_lsm9ds1
import adafruit_sgp30

#Motors
class Motor:
    def _init_(self, pinNum):
        GPIO.setup(pinNum, GPIO.OUTPUT)
        GPIO.OUTPUT(pinNum, GPIO.HIGH)
        self.pwm = GPIO.PWM(pinNum, 1000)
        
    def move_forward(self, dutycycle):
        self.pwm.start(dutycycle)
    # def move_backward():
    #     return


#IMU
def init_IMU():
    
    return

def read_IMU():
    return

def temperature():
    return

#Ultrasonic
def init_ultrasonic():
    return

def distance():
    return

#Dust Sensor
def dssensor():
    return

def light_intensity():
    return

#Thermal Camera
def thermal_camera():
    return

def human_detection():
    return

#Gas Sensor
def init_gassensor():
    return

def eCO2():
    return

def VOC():
    return

#GPS
def init_gps():
    return

def location():
    return
