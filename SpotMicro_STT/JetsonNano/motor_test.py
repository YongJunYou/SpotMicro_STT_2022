from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

import board
import busio
import time

i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))

pca_1 = PCA9685(i2c_bus0, address=0x40)
pca_1.frequency = 60

servo1 = servo.Servo(pca_1.channels[0], min_pulse=450, max_pulse=2750)
servo2 = servo.Servo(pca_1.channels[1], min_pulse=450, max_pulse=2750)
servo3 = servo.Servo(pca_1.channels[2], min_pulse=450, max_pulse=2750)
servo4 = servo.Servo(pca_1.channels[3], min_pulse=450, max_pulse=2750)
servo5 = servo.Servo(pca_1.channels[4], min_pulse=450, max_pulse=2750)
servo6 = servo.Servo(pca_1.channels[5], min_pulse=450, max_pulse=2750)



sweep = range(1, int(180), +1)
sweep_backward = range(int(180), 1, -1)
while True:
    for degree in sweep :
        print(degree)
        servo1.angle = int(degree)
        servo2.angle = int(degree)
        servo3.angle = int(degree)
        servo4.angle = int(degree)
        servo5.angle = int(degree)
        servo6.angle = int(degree)

        time.sleep(0.01)
    for degree in sweep_backward:
        print(degree)
        servo1.angle = int(degree)
        servo2.angle = int(degree)
        servo3.angle = int(degree)
        servo4.angle = int(degree)
        servo5.angle = int(degree)
        servo6.angle = int(degree)

        print( servo2.angle )
        time.sleep(0.01)