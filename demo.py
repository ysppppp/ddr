import DRR
import time
import board
import busio
i2c = DRR.busio.I2C(DRR.board.SCL, DRR.board.SDA)

TRIG = 22
ECHO = 23

#motor
motor1 = DRR.Motor(18)
motor1.move_forward(50)
DRR.time.sleep(5)
motor1.stop()

#imu
accgyro = DRR.Sensor(i2c)
#print(accgyro.read_IMU())

#ultrasonic
us_dis = DRR.Ultrasonic(TRIG, ECHO)
#print(us_dis.distance())

#dust sensor(photodiode)
dss = DRR.Dsensor()
#print(format(dss.readVal()[2], '#010b'))

#Thermal Camera
Tcam = DRR.Thermal_Cam(i2c)
#print(Tcam.readVal())

#Gas Sensor
aqs = DRR.AQSensor(i2c)
def aqsVal():
    count = 0
    for i in range(10):
        count += 1
        print(aqs.readVal()[0:2])
        if count == 10:
            count = 0
            print(aqs.readVal()[2],'  ',aqs.readVal()[3])

#gps
gps = DRR.GPS()
while 1:
    print(accgyro.read_IMU())
    print(us_dis.distance())
    print(format(dss.readVal()))
    print(Tcam.readVal())
    aqsVal()
    gps.readVal()
    time.sleep(3)
