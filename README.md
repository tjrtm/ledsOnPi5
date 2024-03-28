# ledsOnPi5
Controlling led brightness depending on face from camera distance

______________________________________________________________________________________

# set up info

sudo apt install python3-spidev

sudo apt install python3-opencv



_______________________________________________________________________________________


distance.py - main program

fire.py - fireplace animation for a led matrix (square 10x7 leds with left/right sides). 

led_mapping.py - led matrix layout and mapping for text and numbers

Neopixel led strip data wire connected to MOSI pin on raspberry PI 5

Camera connected to raspberry pi usb port

using neopixel_spidev

using openCV (haarcascade_frontalface_default.xml included in repo) for face detection and distance calculation

no drawing, so it works in terminal

webUI.py a flask web service with basic led strip controls
