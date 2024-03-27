import time
import lib.neopixel_spidev as np
import random

LED_COUNT = 79
BRIGHTNESS = 1.0  # Set brightness (0.0 to 1.0)
STRIP_TYPE = np.GRB

pixels = np.NeoPixelSpiDev(0, 0, brightness=BRIGHTNESS, n=LED_COUNT, pixel_order=np.GRB) 

def rand_range(min, max):
    return random.randint(min, max)

def adjust_color(current_color, target_color):
    if current_color < target_color:
        return current_color + 1
    elif current_color > target_color:
        return current_color - 1
    else:
        return current_color

def fireplace_effect():
    target_red = [rand_range(100, 255) for _ in range(LED_COUNT)]
    target_green = [rand_range(0, 60) for _ in range(LED_COUNT)]
    green_led_position = LED_COUNT  # Initialize outside of visible range
    last_update_time = time.time()

    while True:
        current_time = time.time()
        
        # Update the green LED's position every second
        if current_time - last_update_time >= 1:
            green_led_position = rand_range(0, LED_COUNT - 1)
            last_update_time = current_time

        for i in range(LED_COUNT):
            current_color = pixels[i]
            red = adjust_color(current_color[0], target_red[i])
            green = adjust_color(current_color[1], target_green[i])
            blue = 0  # Keep blue component off for the fire effect

            pixels[i] = (red, green, blue)

            # Randomly adjust target colors for dynamic effect
            if random.randint(0, 9) == 0:
                target_red[i] = rand_range(100, 255)
                target_green[i] = rand_range(0, 60)

        pixels.show()
        time.sleep(0.01)  # Adjust for desired effect speed

fireplace_effect()
