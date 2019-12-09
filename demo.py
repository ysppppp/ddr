import DRR
import time
motor1 = DRR.Motor(18)
motor1.move_forward(50)
time.sleep(5)
motor1.stop()