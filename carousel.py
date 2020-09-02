"""
Be sure to check the learn guides for more usage information.
 
This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
 
Author(s): Melissa LeBlanc-Williams for Adafruit Industries

Make sure Python installation of RGB display libraries is installed before using this code:

sudo pip3 install adafruit-circuitpython-rgb-display
sudo apt-get install python3-pip
sudo apt-get install ttf-dejavu
sudo apt-get install python3-pil

Note: ttf-dejavu only used if drawing with this font

"""

import digitalio
import board
import time
from PIL import Image, ImageDraw, ImageFont

#import adafruit_rgb_display.ili9341 as ili9341
#import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
#import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
#import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
#import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

IMAGE_SOURCE=''
FONT = "freefont/FreeSans.ttf"
ttffont34 = ImageFont.truetype("/usr/share/fonts/truetype/"+FONT, 34)
ttffont20 = ImageFont.truetype("/usr/share/fonts/truetype/"+FONT, 20)

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D24)
reset_pin = digitalio.DigitalInOut(board.D25)
 
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 32000000
 
# Setup SPI bus using hardware SPI:
spi = board.SPI()
 
# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
disp = st7735.ST7735R(spi, rotation=90, bgr=True, x_offset=2, y_offset=1,                         # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, height=130, x_offset=0, y_offset=0,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
# disp = ili9341.ILI9341(
#    spi,
#    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
 
# Create blank image for drawing.
if disp.rotation % 180 == 90:
    scheight = disp.width  # we swap height/width to rotate it to landscape!
    scwidth = disp.height
else:
    scwidth = disp.width  # we swap height/width to rotate it to landscape!
    scheight = disp.height
    

def slide_file(showtime, image_file):
    image = Image.open(IMAGE_SOURCE + image_file)
    
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = scwidth / scheight
    if screen_ratio < image_ratio:
        scaled_width = image.width * scheight // image.height
        scaled_height = scheight
    else:
        scaled_width = scwidth
        scaled_height = image.height * scwidth // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    x = scaled_width // 2 - scwidth // 2
    y = scaled_height // 2 - scheight // 2
    image = image.crop((x, y, x + scwidth, y + scheight))
    
    start_time = time.time()
    while((start_time+showtime)>time.time()):
        disp.image(image)

def draw_rotated_text(image, text, x, y, angle, font, fill=white):
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', font.getsize(text), (0,0,0,0))
    textdraw = ImageDraw.Draw(textimage)
    # Render the text.
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, (x, y), rotated)

    
def get_cpu_temp():
    f = open("/sys/class/thermal/thermal_zone0/temp", "r")
    temp = float(f.readline())/1000
    return str(int(temp))

def display_time_temp(showtime, info1, info2):
    start_time = time.time()
    # Make sure to create image with mode 'RGB' for full color.
    image = Image.new("RGB",(scwidth,scheight))
    draw = ImageDraw.Draw(image)

    while((start_time+showtime)>time.time()):
        draw.rectangle((0,0,scwidth,scheight), fill=blue)
        draw.text((10,10), time.strftime("%H:%M:%S"), font=ttffont34, fill=white)
        draw.text((10,50), info1, font=ttffont20, fill=white)
        draw.text((10,70), info2, font=ttffont20, fill=white)
        draw.text((10,90), "Temp = "+get_cpu_temp()+"°C", font=ttffont20, fill=white)
        #draw_rotated_text(image, time.strftime("%H:%M:%S"), 10, 10, 0, ttffont34, fill=white)
        #draw_rotated_text(image, info1, 10, 50, 0, ttffont20, fill=white)
        #draw_rotated_text(image, info2, 10, 70, 0, ttffont20, fill=white)
        #draw_rotated_text(image, "Temp = "+get_cpu_temp()+"°C", 10, 90, 0, ttffont20, fill=white)
        disp.image(image)
        
#main loop
while(True):
    display_time_temp(10,"Tim Skillman","Class 1")
    slide_file(5,"dartmoor.jpg")
    slide_file(5,"cat.jpg")
