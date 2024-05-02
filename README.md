# ledsOnPi5
Controlling led brightness depending on face from camera distance

______________________________________________________________________________________

# set up info

neopixel_spidev.py (included in /lib/)

sudo apt install python3-opencv

_______________________________________________________________________________________


distance.py - main program

fire.py - fireplace animation for a led matrix (square 10x7 leds with left/right sides). 

## Fireplace Effect with NeoPixel LEDs

This Python script simulates a fireplace effect using NeoPixel LEDs. It creates a dynamic and realistic fire animation by adjusting the color and brightness of individual LEDs.

### Dependencies

- `lib.neopixel_spidev`: A library for controlling NeoPixel LEDs using the SPI interface.
- `random`: A library for generating random numbers.
- `time`: A library for time-related functions.

### Configuration

- `LED_COUNT`: The number of NeoPixel LEDs in the strip.
- `BRIGHTNESS`: The overall brightness of the LEDs (0.0 to 1.0).
- `STRIP_TYPE`: The type of NeoPixel LED strip (e.g., `np.GRB`).

### Usage

1. Connect the NeoPixel LED strip to the Raspberry Pi.
2. Install the required dependencies.
3. Run the `fireplace_effect()` function to start the animation.

### Explanation

- The script initializes the NeoPixel strip and sets the initial colors and positions of the LEDs.
- The `fireplace_effect()` function continuously updates the colors and positions of the LEDs to create the fire effect.
- The `rand_range()` function generates a random number within a specified range.
- The `adjust_color()` function adjusts the color of an LED towards a target color.
- The script uses a nested loop to iterate through each LED and update its color and brightness.
- The `time.sleep()` function controls the speed of the animation.

### Customization

- You can adjust the `LED_COUNT`, `BRIGHTNESS`, and `STRIP_TYPE` values to match your specific NeoPixel LED strip.
- You can modify the `fireplace_effect()` function to create different fire effects, such as changing the color palette or the speed of the animation.
- You can add additional features, such as sound effects or user interaction, to enhance the experience.


led_mapping.py - led matrix layout and mapping for text and numbers

Neopixel led strip data wire connected to MOSI pin on raspberry PI 5

Camera connected to raspberry pi usb port

using neopixel_spidev

using openCV (haarcascade_frontalface_default.xml included in repo) for face detection and distance calculation

no drawing, so it works in terminal

webUI.py a flask web service with basic led strip controls
