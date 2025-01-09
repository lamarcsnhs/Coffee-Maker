import RPi.GPIO as GPIO
import time

# distanceToCheck = 4
# pulse_start = 0
# pulse_end = 0

# Front sensor
trg1 = 18
echo1 = 12

# Inits GPIO unit for sensor
def initGPIO(trg, echo):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(echo, GPIO.IN)
    GPIO.setup(trg, GPIO.OUT)

def doesCupExist(distanceToCheck):
    initGPIO(trg1, echo1)


    GPIO.output(trg1, GPIO.LOW)
    time.sleep(0.1)

    
    GPIO.output(trg1, GPIO.HIGH)
    time.sleep(0.00001) 
    GPIO.output(trg1, GPIO.LOW)


    
    while GPIO.input(echo1) == GPIO.LOW:
        pulse_start = time.time()
    # else:
    #     pulse_start = time.time()


    while GPIO.input(echo1) == GPIO.HIGH:
        pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 
    
    print(distance)
    return distance <= distanceToCheck

try:
    while True:
        time.sleep(1) 
        # print("test")
        # distance = doesCupExist(4)
        # print("Distance:", distance, "cm")
        print(doesCupExist(4))
except KeyboardInterrupt:
    GPIO.cleanup()