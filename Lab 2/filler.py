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

#################################################################################
def drawSheep(width, height, rhue, ghue,bhue):
    
    # format is xstart = start x position.   xend = start position + thickness
    thickness = width * .03
    offset1 = (width * .0125)
    
    # y+ goes down, x+ goes right
    draw.rectangle(((width*.1125), (height*.63)+thickness, (width*.125), (height*.75)), outline=0, fill=(rhue,ghue,bhue))
    draw.rectangle(((width*.1375),(height*.63)+thickness,(width*.15),(height*.75)), outline=0, fill=(255,255,255)),
    draw.ellipse(((width * .1),(height * .65),(width * .1) + thickness,(height * .65) + thickness), outline=None,fill=(255,255,255)), # LL
             #canvas.create_oval((width * .1125),(height * .64),(width * .1125) + thickness,(height * .64) + thickness, outline=None,fill="#FFFFFF"), #LM
             #canvas.create_oval((width * .125),(height * .65),(width * .125) + thickness,(height * .65) + thickness, outline=None,fill="#FFFFFF"), #LR
             #canvas.create_oval((width * .1),(height * .60),(width * .1) + thickness,(height * .60) + thickness, outline=None,fill="#FFFFFF"), #UL
             #canvas.create_oval((width * .1125),(height * .59),(width * .1125) + thickness,(height * .59) + thickness, outline=None,fill="#FFFFFF"), #UM
             #canvas.create_oval((width * .125),(height * .60),(width * .125) + thickness,(height * .60) + thickness, outline=None,fill="#FFFFFF"), #UR
             #canvas.create_oval((width * .14),(height * .57),(width * .14) + thickness,(height * .57) + thickness, outline=None,fill="#FFFFFF")) 
##################################################################################

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

####################################################

# calculate these values once instead of inside the timer
q1 = width / 4
q2 = (width / 4) * 2
q3 = (width / 4) * 3

h1 = height / 3
h2 = (height / 3) * 2

if width > height:
    bounder = height
else:
    bounder = width
center = bounder / 2

#####################################################

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    
    # get seconds, minutes, and hour as integer values
    sectime = int(time.localtime().tm_sec)
    mintime = int(time.localtime().tm_min)
    hrtime = int(time.localtime().tm_hour)
    
    rhue = sectime * 4
    ghue = mintime * 4    
    bhue = hrtime * 10
    

        #draw.ellipse((center-40,center+10,center+40,center+40),outline=(rhue,ghue,bhue),fill=(rhue,0,0),width=3)
   
    
    draw.rectangle((0, (height*.75), width, height), outline=0, fill=(rhue,ghue,bhue))
    
    drawSheep(width, height, rhue, ghue, bhue)
    
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)