import RPi.GPIO as GPIO
import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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
    
    while True:
        #draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        #draw.text((0,10), 'Welkom', font= ImageFont.truetype("DejaVuSans.ttf", 23))
        #disp.image(image)
        #disp.display()
        
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        draw.text((19,10), 'Doos is ', font= ImageFont.truetype("DejaVuSans.ttf", 12))
        draw.text((14,20), 'geopend ', font= ImageFont.truetype("DejaVuSans.ttf", 12))
        disp.image(image)
        disp.display()
finally:
    GPIO.cleanup()