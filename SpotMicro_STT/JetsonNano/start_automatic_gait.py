"""
Simulation of SpotMicroAI and it's Kinematics 
Use a keyboard to see how it works
Use keyboard-Button to switch betweek walk on static-mode
"""
from os import system, name 
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import matplotlib.animation as animation
import numpy as np
import time
import math
import datetime as dt
import keyboard
import random

#import Kinematics.kinematics as kn
import spotmicroai
import servo_controller_fix

from multiprocessing import Process
from Common.multiprocess_kb import KeyInterrupt
from Common.multiprocess_mic import MicInterrupt

from Kinematics.kinematicMotion import KinematicMotion, TrottingGait

rtime=time.time()

def reset():
    global rtime
    rtime=time.time()    

robot=spotmicroai.Robot(False,False,reset)
controller = servo_controller_fix.Controllers()

# TODO: Needs refactoring
speed1=240
speed2=170
speed3=300

speed1=322
speed2=237
speed3=436

spurWidth=robot.W/2+20
stepLength=0
stepHeight=72

# Initial End point X Value for Front legs 
iXf=120

walk=False

def resetPose():
    # TODO: globals are bad
    global joy_x, joy_z, joy_y, joy_rz, joy_z
    joy_x, joy_y, joy_z, joy_rz = 128, 128, 128, 128

# define our clear function 
def consoleClear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 



Lp = np.array([[iXf, -100, spurWidth, 1], [iXf, -100, -spurWidth, 1],
[-50, -100, spurWidth, 1], [-50, -100, -spurWidth, 1]])

motion=KinematicMotion(Lp)
resetPose()

trotting=TrottingGait()

def main(id, command_status, stop_status):  # 
    jointAngles = []
    while True:
        
        xr = 0.0
        yr = 0.0

        # Reset when robot pose become strange
        # robot.resetBody()
    
        ir=xr/(math.pi/180)
        
        d=time.time()-rtime

        # robot height
        height = 40

        # calculate robot step command from keyboard inputs
        result_dict = command_status.get() #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 멀티프로세스로 가져옴
        result_dict_mic = stop_status.get()
        print(result_dict)
        print(result_dict_mic)
        command_status.put(result_dict)
        stop_status.put(result_dict_mic)

        # wait 3 seconds to start
        if result_dict['StartStepping'] and not result_dict_mic['Wait']:
            currentLp = trotting.positions(d-3, result_dict)# 여기서 가져온 결과를 사용하여 키네마틱 모션에서 사용함
            robot.feetPosition(currentLp)
        else:
            robot.feetPosition(Lp)
        #roll=-xr
        roll=0
        robot.bodyRotation((roll,math.pi/180*((joy_x)-128)/3,-(1/256*joy_y-0.5)))
        bodyX=50+yr*10
        robot.bodyPosition((bodyX, 40+height, -ir))

        # Get current Angles for each motor
        jointAngles = robot.getAngle()
        print(jointAngles)
        
        # First Step doesn't contains jointAngles
        if len(jointAngles):
            # Real Actuators
            controller.servoRotate(jointAngles)
            
            # # Plot Robot Pose into Matplotlib for Debugging
            # TODO: Matplotplib animation
            # kn.initFK(jointAngles)
            # kn.plotKinematics()

        robot.step()
        consoleClear()


if __name__ == "__main__":
    try:
        # Keyboard input Process
        KeyInputs = KeyInterrupt()
        KeyProcess = Process(target=KeyInputs.keyInterrupt, args=(1, KeyInputs.key_status, KeyInputs.command_status))
        KeyProcess.start()

        # Speech input Process #My code
        MicInputs = MicInterrupt() 
        MicProcess = Process(target=MicInputs.micInterrupt, args=(2, MicInputs.stop_status))
        MicProcess.start()


        # Main Process 
        main(3, KeyInputs.command_status, MicInputs.stop_status)# 여기서 키보드인풋가져오는데, 옆에 스피치 인풋   # 

        print("terminate KeyBoard Input process")
        if KeyProcess.is_alive():
            KeyProcess.terminate()
    except Exception as e:
        print(e)
    finally:
        print("Done... :)")