import RPi.GPIO as GPIO
import time   

# Front sensor
trigger_pin_1 = 18
echo_pin_2 = 12

# Constant
SPEED_OF_SOUND_CM_S = 34416 # speed of sound constant at 71 deg F, just took the avg for best precision

# Inits GPIO unit for sensor
def initGPIO(trg, echo):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(echo, GPIO.IN)
    GPIO.setup(trg, GPIO.OUT)

def getDistance(trg, echo, timeout = 0.01): # trigger/echo pins of sensor, timeout in sec
    # Sends a pulse to trigger the sensor
    GPIO.output(trg, True)
    time.sleep(0.00001)
    GPIO.output(trg, False)

    # Waits for the echo response
    pulse_start = time.time()
    pulse_end = time.time()
    
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
        if pulse_start - start_time > timeout:
            return None  # no echo received

    pulse_end = pulse_start
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
        if pulse_end - pulse_start > timeout:
            return None  # echo too long

    # Calculates pulse duration to get distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * SPEED_OF_SOUND_CM_S / 2 # division by two in order to get the one way distance time, as it gives the roundtrip without it
    distance = round(distance, 2)

    return distance

# For front sensor
initGPIO(trigger_pin_1, echo_pin_2)

try:
    while True:
        distance = getDistance(trigger_pin_1, echo_pin_2)
        print("Distance:", distance, "cm")
except KeyboardInterrupt:
    GPIO.cleanup()
