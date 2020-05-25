import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import _thread

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM)

try:
    # Display
    DC = 23 	# data/control
    RST = 24 	# reset
    SPI_PORT = 0	 # SPI port 0	
    SPI_DEVICE = 1  # CS1 pin26
    disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT)) 
    disp.begin(contrast=60)
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)

    # RFID reader
    reader = SimpleMFRC522()
    idKaarten = (71815051611621262605124040505121, 71815051611621262605124040505122, 71815051611621262605124040505123)
    text = 0
    
    # Buzzer
    buzzer_GPIO = 18
    GPIO.setup(buzzer_GPIO, GPIO.OUT)
    buzzer = GPIO.PWM(buzzer_GPIO, 1)
    doBuzzerCompleteOnce = False
    
    # Servo motor
    GPIO.setup(4, GPIO.OUT)
    p = GPIO.PWM(4, 50)


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
        time.sleep(shortStop/2)
        buzzer.start(50)
        
        buzzer.ChangeFrequency(1050)
        time.sleep(shortStop)
        
        buzzer.stop()
        time.sleep(shortStop/2)
        buzzer.start(50)
        
        buzzer.ChangeFrequency(1050)
        time.sleep(shortStop)
        
        buzzer.stop()
        time.sleep(shortStop/2)
        buzzer.start(50)
        
        buzzer.ChangeFrequency(1050)
        time.sleep(shortStop)
        
        buzzer.stop()
        time.sleep(shortStop/2)
        buzzer.start(50)
        
        buzzer.ChangeFrequency(1075)
        time.sleep(longStop)
        buzzer.stop()


    def open_doos():
        p.start(7.5)
        
        p.ChangeDutyCycle(11)
        time.sleep(.75)
        p.ChangeDutyCycle(0)
        p.stop()
    

    for i in range(0, len(idKaarten)):
        while True:
            draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
            draw.text((31,10), str(i + 1) , font= ImageFont.truetype("DejaVuSans.ttf", 23))
            disp.image(image)
            disp.display()

            #print("Geef kaart",i + 1)
            id, text = reader.read()
            #print("id:",id)
            #print("text:", text)
            #print("Nodige kaart:",idKaarten[i])
            if text is None or text is '' or text is ' ':
                text = 0
            if int(text) == idKaarten[i]:
                #print("JUIST\n")
                buzz_good()
                i += 1
                break
            else:
                #print("foute kaart\n")
                buzz_bad()
            time.sleep(0.5)
    
    _thread.start_new_thread(buzz_complete, ())
    _thread.start_new_thread(open_doos, ())
    while True:
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        draw.text((19,10), 'Doos is ', font= ImageFont.truetype("DejaVuSans.ttf", 12))
        draw.text((14,20), 'geopend ', font= ImageFont.truetype("DejaVuSans.ttf", 12))
        disp.image(image)
        disp.display()
        
        
finally:
    GPIO.cleanup()
