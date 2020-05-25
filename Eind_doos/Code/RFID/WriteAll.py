import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

try:
    vraag = input("Wil je naar een RFID badge en kaart schrijven? [J/N]")
    while vraag.lower() == 'j':
        text = input('New data:')
        print("plaats badge")
        reader.write(text)
        print("Geschreven!")
        time.sleep(1)
        print("plaats kaart")
        reader.write(text)
        print("Geschreven!")
        vraag = input("\nWil nog één schrijven? [J/N]")
finally:
        GPIO.cleanup()