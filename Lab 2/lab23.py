import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

q1 = width / 4
q2 = (width / 4) * 2
q3 = (width / 4) * 3

if width > height:
    bounder = height
else:
    bounder = width
center = bounder / 2


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    sectime = int(time.localtime().tm_sec)
    mintime = int(time.localtime().tm_min)
    hrtime = int(time.localtime().tm_hour)
    
    ghue = sectime * 4    
    rhue = mintime * 4
    bhue = hrtime * 10
    
    draw.ellipse((center-60,center-60,center+60,center+60),outline=(rhue,ghue,bhue), fill=(None))
    
    if sectime >= 0 and sectime <= 59: # left eye
        draw.ellipse((center-40,center-40,center-10,center-10),outline=(rhue,ghue,bhue), fill=(None))
    if sectime >= 10 and sectime <= 59: # right eye
        draw.ellipse((center+10,center-40,center+40,center-10),outline=(rhue,ghue,bhue), fill=(None))
    if sectime >= 20 and sectime <= 59: #left ball
        draw.ellipse((center-32,center-24,center-18,center-10),outline=(rhue,ghue,bhue), fill=(0,0,bhue))
    if sectime >= 30 and sectime <= 59: # right ball
        draw.ellipse((center+18,center-24,center+32,center-10),outline=(rhue,ghue,bhue), fill=(0,0,bhue))
    if sectime >= 40 and sectime <= 59: # lips
        #draw.arc((center-40,center+10,center+40,center+40),start=1,end=-1,fill=(rhue,0,0),width=3)
        #draw.arc((center-40,center+10,center+40,center+40),start=.5,end=-.5,fill=(rhue,0,0),width=3)
        draw.ellipse((center-40,center+10,center+40,center+40),fill=(rhue,0,0),width=3)
    
    
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)