import RPi.GPIO as GPIO
import time
import random
import os
from mfrc522 import SimpleMFRC522

time.sleep(60)              # Wait until full system has started to prevent bugs

GPIO.setmode(GPIO.BCM)

reader = SimpleMFRC522()

buzzer_pin = 21
GPIO.setup(buzzer_pin, GPIO.OUT)
buzzer = GPIO.PWM(buzzer_pin, 1)

motor_pin = 17
GPIO.setup(motor_pin, GPIO.OUT)
motor = GPIO.PWM(motor_pin, 50)
motor.start(0)

btn_reset = 18
btn_reset_state = 0
led_reset = 22
btns = (20, 16, 12, 24, 23)
btns_state = [0, 0, 0, 0, 0]
leds = (26, 19, 13, 6, 5)
leds_state = [0, 0, 0, 0, 0]

GPIO.setup(btn_reset, GPIO.IN)
GPIO.setup(led_reset, GPIO.OUT)

for i in range(len(btns)):
    GPIO.setup(btns[i], GPIO.IN)
    
for i in range(len(leds)):
    GPIO.setup(leds[i], GPIO.OUT)


def buzz_good():
    buzzer.start(50)
    buzzer.ChangeFrequency(1200)
    time.sleep(0.1)
    buzzer.stop()
    
    
def buzz_bad():
    buzzer.start(50)
    buzzer.ChangeFrequency(200)
    time.sleep(0.4)
    buzzer.ChangeFrequency(150)
    time.sleep(0.4)
    buzzer.ChangeFrequency(100)
    time.sleep(0.4)
    buzzer.stop()
    
    
def toggle(i):
    if i == 1:
        i = 0
    else:
        i = 1
    return i


def change_leds(i):
    if i == 0:
        leds_state[0] = toggle(leds_state[0])
        leds_state[1] = toggle(leds_state[1])
    elif i == 1:
        leds_state[1] = toggle(leds_state[1])
        leds_state[3] = toggle(leds_state[3])
    elif i == 2:
        leds_state[2] = toggle(leds_state[2])
        leds_state[4] = toggle(leds_state[4])
    elif i == 3:
        leds_state[1] = toggle(leds_state[1])
        leds_state[2] = toggle(leds_state[2])
        leds_state[4] = toggle(leds_state[4])
    else:
        leds_state[2] = toggle(leds_state[2])
        leds_state[3] = toggle(leds_state[3])
    sync_leds()

        
def sync_leds():
    global win
    for i in range(len(leds)):
        GPIO.output(leds[i], leds_state[i])
    if not 0 in leds_state:
        win = True
        
        
def sync_btns():
    global btn_reset_state
    for i in range(len(btns)):
        btns_state[i] = GPIO.input(btns[i])
    btn_reset_state = GPIO.input(btn_reset)
        
        
def reset_leds():
    for i in range(len(leds_state)):            # Turn all leds off
        leds_state[i] = 0
    sync_leds()
        
        
def led_reset_flicker():
    for i in range(3):
        GPIO.output(led_reset, 1)
        time.sleep(0.15)
        GPIO.output(led_reset, 0)
        time.sleep(0.15)
        
        
def unlock():                                   # 0 = unlocked
    global position_motor                       # 1 = locked
    if position_motor == "1":
        motor.ChangeDutyCycle(6.1)
        time.sleep(0.15)
        motor.ChangeDutyCycle(0)
        position_motor = "0"
        with open("/home/pi/EscapeRoom/position_motor", "w") as file:
            file.write(str(position_motor))


def lock():
    global position_motor
    if position_motor == "0":
        motor.ChangeDutyCycle(7.9)
        time.sleep(0.15)
        motor.ChangeDutyCycle(0)
        position_motor = "1"
        with open("/home/pi/EscapeRoom/position_motor", "w") as file:
            file.write(str(position_motor))


code = str(random.randint(1000000000, 9999999999))
win = False

try:
    sync_btns()
    reset_leds()
    position_motor = ""
    with open("/home/pi/EscapeRoom/position_motor") as file:        # Motor sync
        position_motor = file.read().rstrip()
    unlock()
    
    led_reset_flicker()
    reader.write(code)              # Write code to tag
    buzz_good()
    time.sleep(1)
    lock()
    time.sleep(5)

    id, tag = reader.read()         # Read code from tag
    while code not in tag:
        buzz_bad()
        time.sleep(1)
        id, tag = reader.read()
    
    buzz_good()                     # Start game
    for i in range(len(leds)):
        GPIO.output(leds[i], 1)
        time.sleep(0.15)
    led_reset_flicker()
    time.sleep(0.5)
    reset_leds()
    sync_btns()
    
    while win == False:
        for i in range(len(btns)):
            if GPIO.input(btns[i]) != btns_state[i]:        # If the state of a button changes
                btns_state[i] = toggle(btns_state[i])
                change_leds(i)
            if GPIO.input(btn_reset) != btn_reset_state:    # If the state of the reset button changes
                btn_reset_state = toggle(btn_reset_state)
                reset_leds()
                led_reset_flicker()
            time.sleep(0.05)
            
    for i in range(3):
        buzz_good()
        time.sleep(0.2)
    unlock()
        
finally:
    GPIO.cleanup()
    os.system("sudo shutdown -h now")