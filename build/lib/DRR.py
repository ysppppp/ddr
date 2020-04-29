import time
import serial
import spidev
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
    def stop(self):
        self.pwm.start(0)
#IMU
class Sensor:
    def __init__(self, i2c):
        self.sensor = IMU.LSM9DS1_I2C(i2c)
    def read_IMU(self):
        mag_x, mag_y, mag_z = self.sensor.magnetic
        gyro_x, gyro_y, gyro_z = self.sensor.gyro
        return mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z

    def read_TEMP(self):
        temp = self.sensor.temperature
        return temp

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
class Dsensor:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 7629
        return

    def readVal(self):
        resp = self.spi.xfer2([0b01101000, 0b00000000])
        temp = resp[0]*1000+resp[1]
        res = bin(temp)
        return res

#dss = Dsensor()
#while 1:
#    print(format(dss.readVal()))
#    time.sleep(1)

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
class GPS:
    def __init__(self):
        self.ser = serial.Serial ("/dev/ttyS0", 9600)

    def readVal(self):
        res = 0
        received_data = self.ser.read()              #read serial port
        time.sleep(0.03)
        data_left = self.ser.inWaiting()             #check for remaining byte
        received_data += self.ser.read(data_left)
        a = received_data.decode("utf-8").split(",")
        #Cycle through data here
        for i in range(len(a)):

            if(a[i] == "$GNGGA"):
                gpsData = {
                "ts" : a[i+1],
                "lat" : a[i+2],
                "latDir" : a[i+3],
                "long" : a[i+4],
                "longDir" : a[i+5],
                "fix" : a[i+6]

        }
            # print gpsData
            return gpsData
