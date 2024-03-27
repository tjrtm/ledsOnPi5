# ledsOnPi5
Controlling led brightness depending on face from camera distance

# set up
-- Neopixel led strip data wire connected to MOSI pin on raspberry PI 5 
-- Camera connected to raspberry pi usb port
-- using neopixel_spidev
-- using openCV (haarcascade_frontalface_default.xml included in repo) for face detection and distance calculation
-- no drawing, so it works in terminal
