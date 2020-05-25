import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)

p = GPIO.PWM(4, 50)

p.start(7.5)

try:
    while True:
        p.ChangeDutyCycle(11)
        time.sleep(0.75) # sleep 0.28 seconds
        p.ChangeDutyCycle(0)  # turn towards 0 degree
        time.sleep(1) # sleep 1 second
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
