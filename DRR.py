import time
import RPi.GPIO as GPIO
import busio
import board
import adafruit_amg88xx as TCAM
import adafruit_lsm9ds1 as IMU
import adafruit_sgp30 as AQS

i2c = busio.I2C(board.SCL, board.SDA)
#Motors
class Motor:
    def __init__(self, pinNum):
        GPIO.setup(pinNum, GPIO.OUT)
        GPIO.output(pinNum, GPIO.LOW)
        self.pwm = GPIO.PWM(pinNum, 1000)
        
    def move_forward(self, dutycycle):
        self.pwm.start(dutycycle)
    # def move_backward():
    #     return
#IMU
class Sensor:
    def __init__(self, i2c):
        self.sensor = IMU.LSM9DS1_I2C(i2c)
    def read_IMU(self):
        self.mag_x, self.mag_y, self.mag_z = self.sensor.magnetic
        self.gyro_x, self.gyro_y, self.gyro_z = self.sensor.gyro
        self.temp = self.sensor.temperature

#Ultrasonic
class Ultrasonic:
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        GPIO.output(trig, False)
        time.sleep(2)

    def distance(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        while GPIO.input(self.echo)==0:
            pulse_start = time.time()
        while GPIO.input(self.echo)==1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return distance
#dis = Ultrasonic(22,23)
#while 1:
#    distance = dis.distance()
#    time.sleep(1)
#    print(distance)

#Dust Sensor
def dssensor():
    return

def light_intensity():
    return

#Thermal Camera
class Thermal_Cam:
    def __init__(self,i2c):
        self.T_Cam = TCAM.AMG88XX(i2c)
    def readVal(self):
        grid = self.T_Cam.pixels
        return grid

#ttt = Thermal_Cam(i2c)
#while(1):
#    print(ttt.readVal())
#    time.sleep(1)
    
#Gas Sensor
class AQSensor:
    def __init__(self, i2c):
        self.gas_sensor = AQS.Adafruit_SGP30(i2c)
        self.gas_sensor.iaq_init()
        self.gas_sensor.set_iaq_baseline(0x8973, 0x8aae)
        
    def readVal(self):
        eCO2 = self.gas_sensor.eCO2
        TVOC = self.gas_sensor.TVOC
        baseline_eCO2 = self.gas_sensor.baseline_eCO2
        baseline_TVOC = self.gas_sensor.baseline_TVOC
        return eCO2, TVOC, baseline_eCO2, baseline_TVOC
#sss = AQSensor(i2c)
#count = 0
#while 1:
#    count += 1
#    print(sss.readVal()[0:2])
#    if count == 10:
#        count = 0
#        print(sss.readVal()[2],'  ',sss.readVal()[3])
#

#GPS
def init_gps():
    return

def location():
    return
