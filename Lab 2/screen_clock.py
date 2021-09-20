import subprocess
import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565
import webcolors

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

# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

countup_timer = 0
countdown_timer = 22075000
penalties_tracker = 0
bonuses_tracker = 0

IP = "line test 1"
PENALTIES = "PENALTIES: "
BONUSES = "BONUSES: "
LIVED   = "LIVED: "
TO_LIVE = "TO_LIVE: "


while True:
   # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    
    # penalties tracker 
    if buttonA.value and not buttonB.value:
        penalties_tracker   += 1
        countdown_timer     -= 1000
        disp.fill(color565(255,0,0))
    
    if buttonB.value and not buttonA.value:
        bonuses_tracker     += 1
        countdown_timer     += 1000
        disp.fill(color565(0,255,0))
    
    if not buttonA.value and not buttonB.value:
        disp.fill(color565(0,0,0))
    

    # Write four lines of text.
    # draw.text((x, y), IP, font=font, fill="#FFFFFF")
    x = 0
    y = top
    y += font.getsize(IP)[1]
    draw.text((x, y), LIVED, font=font, fill="#44c17b")
    x = font.getsize(LIVED)[0]
    draw.text((x, y), str(countup_timer), font=font, fill="#FFFF00")
    
    x = 0
    y += font.getsize(IP)[1]
    draw.text((x, y), TO_LIVE, font=font, fill="#20b2aa")
    x = font.getsize(TO_LIVE)[0]
    draw.text((x, y), str(countdown_timer), font=font, fill="#FFFF00")
    
    x = 0
    y += font.getsize(IP)[1]
    draw.text((x, y), BONUSES, font=font, fill="#20b2aa")
    x = font.getsize(BONUSES)[0]
    draw.text((x, y), str(bonuses_tracker), font=font, fill="#FFFF00")
    
    x = 0
    y += font.getsize(IP)[1]
    draw.text((x, y), "PENALTIES: ", font=font, fill="#FF0000")
    x = font.getsize(PENALTIES)[0]
    draw.text((x, y), str(penalties_tracker), font=font, fill="#FFFF00")

    # Display image.
    disp.image(image, rotation)
    time.sleep(.1)
    countup_timer += 1
    countdown_timer -= 1


