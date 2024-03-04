# EHHHH??? THERE ARE SO FEW RESOURCES FOR THE VELLEMAN WPSE306N
# imma have to run this through ChatGPT tomorrow

import time
import sys
import RPi.GPIO as GPIO
import json 
import threadings
import traceback
from gpiozero import Servo

def sensor():
    trg_pin = 18
    echo_pin = 12

    GPIO.setmode(GPIO.BCM)
        
    print("works?")

sensor()