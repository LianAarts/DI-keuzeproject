import time
import RPi.GPIO as GPIO
from keypad import keypad
from mfrc522 import SimpleMFRC522
import spidev

# lcd
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
import time
import PIL

# lcd
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setup(17, GPIO.OUT)
p = GPIO.PWM(17, 50)

# hardware SPI config:
DC = 16  # data/control
RST = 20  # reset
SPI_PORT = 0  # SPI port 0
SPI_DEVICE = 1  # CS1 pin26

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
disp.begin(contrast=50)
font = ImageFont.truetype("puzzel/DejaVuSans.ttf", 15)
draw = ImageDraw.Draw(image)
# clear the image.
draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
nummer = 4

spi = spidev.SpiDev()  # create spi object
spi.open(0, 0)  # open spi port 0, device CS0 pin 24
spi.max_speed_hz = (1000000)

reader = SimpleMFRC522()

buzzer_pin = 26
GPIO.setup(buzzer_pin, GPIO.OUT)
buzzer = GPIO.PWM(buzzer_pin, 1)

bl_pin = 21
GPIO.setup(bl_pin, GPIO.OUT)
GPIO.output(bl_pin, 1)
kp = keypad(columnCount=3)

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


def buzz_complete():
    shortStop = 0.1
    longStop = 0.4
    buzzer.start(50)
    buzzer.ChangeFrequency(300)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(400)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(500)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(600)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(700)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(800)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(900)
    time.sleep(longStop)
    buzzer.ChangeFrequency(800)
    time.sleep(longStop)
    buzzer.ChangeFrequency(325)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(400)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(425)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(525)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(700)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(725)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(975)
    time.sleep(longStop)
    buzzer.ChangeFrequency(725)
    time.sleep(longStop)
    buzzer.ChangeFrequency(475)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(550)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(650)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(775)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(850)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(950)
    time.sleep(shortStop)
    buzzer.ChangeFrequency(1050)
    time.sleep(longStop)
    buzzer.stop()
    time.sleep(shortStop / 2)
    buzzer.start(50)
    buzzer.ChangeFrequency(1050)
    time.sleep(shortStop)
    buzzer.stop()
    time.sleep(shortStop / 2)
    buzzer.start(50)
    buzzer.ChangeFrequency(1050)
    time.sleep(shortStop)
    buzzer.stop()
    time.sleep(shortStop / 2)
    buzzer.start(50)
    buzzer.ChangeFrequency(1050)
    time.sleep(shortStop)
    buzzer.stop()
    time.sleep(shortStop / 2)
    buzzer.start(50)
    buzzer.ChangeFrequency(1075)
    time.sleep(longStop)
    buzzer.stop()


while True:
    GPIO.setwarnings(False)
    digit = None
    init = False
    rfidGereed = False
    codeGereed = False
    rfidUnlock = False
    number = False
    string = ''
    reset = False
    seq = []

    draw.text((1, 0), '1: use RFID', font=font)
    draw.text((1, 15), '2: no RFID', font=font)
    disp.image(image)
    disp.display()
    print(digit)

    while digit == None:
        digit = kp.getKey()
    if digit == 1:
        useRFID = True
        print('use RFID')

    else:
        useRFID = False
        print('no RFID')

    buzz_good()
    draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
    disp.image(image)
    disp.display()

    if useRFID is True:
        while rfidGereed is False:
            print(useRFID)
            print("place your tag to write")

            draw.text((1, 0), 'place your', font=font)
            draw.text((1, 15), 'tag to', font=font)
            draw.text((1, 30), 'write', font=font)
            disp.image(image)
            disp.display()

            key = str(2204)
            reader.write(key)
            key = int(key)
            buzz_good()

            draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
            print("RFID is ready")

            draw.text((1, 0), 'rfid is', font=font)
            draw.text((1, 15), 'ready', font=font)
            disp.image(image)
            disp.display()

            time.sleep(1)
            draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
            draw.text((1, 0), 'remove', font=font)
            draw.text((1, 15), 'tag', font=font)
            disp.image(image)
            disp.display()
            time.sleep(1)
            draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
            rfidGereed = True


    while codeGereed is False:
        draw.text((1, 0), 'Set the', font=font)
        draw.text((1, 15), 'code', font=font)
        disp.image(image)
        disp.display()

        seq = []
        i = 0
        while i < 4:
            digit = None
            while digit == None:
                digit = kp.getKey()

            if digit == "*":
                seq = []
                print(seq)
                buzz_bad()
                string = ''
                i = 0
            else:
                seq.append(digit)
                string = string + ' ' + str(digit)
                i += 1
            buzz_good()


            draw.text((1, 0), 'Set the', font=font)
            draw.text((1, 15), 'code', font=font)
            draw.text((1, 30), string, font=font)
            disp.image(image)
            disp.display()
            time.sleep(0.4)

            draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
        code = seq
        print(code)

        draw.text((1, 0), 'Code is set', font=font)
        draw.text((1, 15), string, font=font)
        disp.image(image)
        disp.display()
        time.sleep(1)
        string = ''
        GPIO.output(bl_pin, 0)
        draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
        disp.image(image)
        disp.display()

        codeGereed = True

    if useRFID is True:
        while rfidUnlock is False:
            id, text = reader.read()
            print(text)
            print(key)
            if int(text) == key:
                print("unlock")
                GPIO.output(bl_pin, 1)
                buzz_good()
                draw.text((1, 0), 'Unlocked!!', font=font)
                disp.image(image)
                disp.display()
                time.sleep(2)
                draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
                disp.image(image)
                disp.display()
                rfidUnlock = True


    while number == False:
        GPIO.output(bl_pin, 1)
        # Initialize

        ###### 4 Digit wait ######
        seq = []
        i = 0
        while i < 4:
            print(i)
            digit = None
            draw.text((1, 0), 'Enter a', font=font)
            draw.text((1, 15), 'code', font=font)
            disp.image(image)
            disp.display()
            while digit == None:
                digit = kp.getKey()
            if digit == "*":
                seq = []
                print(seq)
                string = ""
                draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
                disp.image(image)
                disp.display()
                i = 0
            else:
                seq.append(digit)
                string = string + ' ' + str(digit)
                i += 1

            buzz_good()

            draw.text((1, 30), string, font=font)
            disp.image(image)
            disp.display()

            time.sleep(0.4)

        draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
        disp.image(image)
        disp.display()

        # Check digit code
        print(seq)
        if seq == code:
            print("Code accepted")
            draw.text((1, 0), 'The code', font=font)
            draw.text((1, 15), 'is correct', font=font)
            draw.text((1, 30), string, font=font)
            disp.image(image)
            disp.display()
            number = True
            buzz_complete()
            p.start(10)  # turn towards 90 degree
            time.sleep(.25)  # sleep 1 second
            p.ChangeDutyCycle(0)  # turn towards 0 degree
            time.sleep(1)
        else:
            print("Wrong code")
            draw.text((1, 0), 'The code is', font=font)
            draw.text((1, 15), 'not correct', font=font)
            draw.text((1, 30), string, font=font)
            disp.image(image)
            disp.display()
            buzz_bad()
            time.sleep(1)
            draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
            disp.image(image)
            disp.display()
            string = ""

    while reset is False:
        print("ready for reset")
        seq = []
        for i in range(3):
            digit = None
            while digit == None:
                digit = kp.getKey()
            buzz_good()
            seq.append(digit)
            print(seq)
            time.sleep(0.4)

        if seq == ['*', 0, '#']:
            print("reset")
            draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
            draw.text((1, 0), 'reset', font=font)
            disp.image(image)
            disp.display()
            time.sleep(1)
            draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
            disp.image(image)
            disp.display()
            reset = True
        else:
            buzz_bad()










