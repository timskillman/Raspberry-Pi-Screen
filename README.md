![alt text](https://github.com/timskillman/Raspberry-Pi-Screen/blob/master/images/Case-pic.png "3D printed case & screen")

# Raspberry-Pi-Screen ReadMe

This repo provides code to run a background carousel of images and info for the supplied 3D printed case

**3D Printed case**

STL files are available in the STL folder of this repo
The case is designed for an ICE Tower Cooler (or OEM equivalent)

*Print settings*

PLA, 0.3 mm layer height, 3 layer wall thickness, top and bottom

**Hardware setup**

The case will fit a 1.8" TFT SPI screen (128x160, ST7735 driver chip).  
These are readily available for a few pounds on eBay (around £2.50+postage)

![alt text](https://github.com/timskillman/Raspberry-Pi-Screen/blob/master/images/st7735screen.png "1.8 inch ST7735 SPI screen")

Here is the wiring diagram to connect the screen to the Raspberry Pi:

![alt text](https://github.com/timskillman/Raspberry-Pi-Screen/blob/master/images/ST7735_128x128_GPIO.png "Wiring Diagram")

**Code for running screen**

Using the latest Raspbian image (Raspbian or Rapberry Pi OS) enable SPI in the device settings;

![alt text](https://github.com/timskillman/Raspberry-Pi-Screen/blob/master/images/EnableSPI.png "Enable SPI")

A single python script and images folder will run a carousel of images on the screen.

The python script uses Adafruit's rgb display drivers that can be installed on your Raspberry Pi with the following commands in a terminal window:

~~~~
sudo pip3 install adafruit-circuitpython-rgb-display
sudo apt-get install python3-pip
sudo apt-get install python3-pil
~~~~

The next thing to do is git clone this repo onto your Raspberry in the pi folder:

~~~~
git clone https://github.com/timskillman/Raspberry-Pi-Screen/
~~~~

Navigate to the folder:

~~~~
cd Raspberry-Pi-Screen
~~~~

And try the carousel.py program with example images on your connected screen:

~~~~
python carousel.py
~~~~

The display should run a carousel of images and information screen showing time, example text and CPU temperature

