import RPi.GPIO as GPIO
import time   

# Front sensor
trigger_pin = 18
echo_pin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(trigger_pin, GPIO.OUT)

def getDistance(trg, echo): # trigger/echo pins of sensor
    # Sends a pulse to trigger the sensor
    GPIO.output(trg, True)
    time.sleep(0.00001)
    GPIO.output(trg, False)

    # Waits for the echo response
    pulse_start = time.time()
    pule_end = time.time()

    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    # Calculates pulse duration to get distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 # speed of sound = 17150 cm/s
    distance = round(distance, 2)

    return distance

try:
    while True:
        distance = getDistance(trigger_pin, echo_pin)
        print("Distance:", distance, "cm")
except KeyboardInterrupt:
    GPIO.cleanup()