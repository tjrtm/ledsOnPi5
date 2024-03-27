import board
import lib.neopixel_spidev as np
import time
import termios, fcntl, sys, os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configuration
NUM_PIXELS = 79
BRIGHTNESS = 1.0
AUTO_WRITE = True
WHITE = (255,255,255)
BLACK = (0,0,0)
import led_mapping
from led_mapping import led_matrix, char_mappings, abc, number_mappings

app = Flask(__name__)

CORS(app)


# Initialize NeoPixel, GRB == RGB
pixels = np.NeoPixelSpiDev(0, 0, brightness=BRIGHTNESS, n=NUM_PIXELS, pixel_order=np.GRB) 

# Initialize LED buffer
LED_BUFFER = [(0, 0, 0) for _ in range(NUM_PIXELS)]

# Function to adjust brightness relative to current level
def adjust_brightness(change):
    # Get current brightness
    current_brightness = pixels.brightness
    print(current_brightness)
    # Calculate new brightness level
    new_brightness = max(0.0, min(1.0, current_brightness + change))
    # Set new brightness, ensuring it stays within the 0.0 to 1.0 range
    pixels.brightness = new_brightness
    on()
    print(f"Brightness adjusted to {new_brightness}")

def rgb_to_brightness(rgb):
    current_brightness = pixels.brightness
    print(current_brightness)
    max_value = max(rgb)  # Find the maximum value in the RGB tuple
    # Map the max value from 10-255 range to 0.01-0.9 range
    brightness = 0.01 + (max_value - 10) * (0.89 / (255 - 10))
    return max(0.01, min(0.9, brightness))  # Ensure brightness is within bounds

def adjust_brightness(change):
    # Get current brightness
    current_brightness = pixels.brightness
    print(current_brightness)
    # Calculate new brightness level and round to one decimal place
    new_brightness = round(max(0.0, min(1.0, current_brightness + change)), 1)
    # Set new brightness, ensuring it stays within the 0.0 to 1.0 range
    pixels.brightness = new_brightness
    on()
    print(f"Brightness adjusted to {new_brightness}")


# Function to set brightness
def set_brightness(brightness_level):
    pixels.brightness = brightness_level

# Function to set an individual LED color
def led_on(led_id, color=WHITE, clear=True):
    if 0 <= led_id < NUM_PIXELS:
        pixels[led_id] = color

def led_off(led_id, color=BLACK, clear=True):
    if 0 <= led_id < NUM_PIXELS:
        pixels[led_id] = color

def on(color=WHITE):
    pixels.fill(color)

def off():
    on((0, 0, 0))

def display_letter(character, color=WHITE):
    char_upper = character.upper()  # Convert to uppercase for consistent lookup

    if char_upper in char_mappings: 
        led_positions = char_mappings[char_upper]
    elif char_upper in number_mappings:
        led_positions = number_mappings[char_upper]
    else: 
        return  # Do nothing if the character is not found in either mapping

    pixels.fill((0, 0, 0)) 
    for pos in led_positions:
        led_on(pos, color)

def display_sentence(sentence, color=(255,255,0), delay=0.05):
    """Displays a sentence letter by letter, with an optional delay between letters.

    Args:
        sentence (str): The sentence to display.
        color (tuple, optional): RGB color tuple for the letters. Defaults to WHITE.
        delay (float, optional): Delay in seconds between displaying each letter. Defaults to 0.5.
    """

    import time  # Import the time module for the delay

    for character in sentence:
        display_letter(character, color)
        time.sleep(delay) 
    off()

def custom_message():
    msg = input('Enter your message: ')
    display_sentence(msg)

fd = sys.stdin.fileno()  # Get file descriptor for standard input

oldterm = termios.tcgetattr(fd)  # Save old terminal settings
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO  # Configure for raw input
termios.tcsetattr(fd, termios.TCSANOW, newattr)

@app.route('/leds/brightness/<float:brightness>', methods=['GET'])
def api_set_brightness(brightness):
    # Ensure the brightness level is within the valid range
    if 0.0 <= brightness <= 0.9:
        set_brightness(brightness)
        return jsonify({"message": f"Brightness set to {brightness}"}), 200
    else:
        return jsonify({"error": "Brightness level must be between 0.0 and 1.0"}), 400

from flask import jsonify  # Make sure to import jsonify at the top of your file

@app.route('/leds/brightness_by_rgb/<rgb>', methods=['GET'])
def adjust_brightness_by_rgb(rgb):
    # Convert the input string to an RGB tuple
    rgb_tuple = tuple(map(int, rgb.split(',')))
    # Calculate the corresponding brightness level
    brightness = rgb_to_brightness(rgb_tuple)
    # Set the new brightness
    pixels.brightness = brightness
    # Return a JSON response indicating success and the new brightness level
    return jsonify({"success": True, "message": f"Brightness adjusted to {brightness:.2f} based on RGB {rgb}"}), 200

 

@app.route('/led/on/<int:led_id>/<color>', methods=['GET'])
def turn_led_on(led_id, color):
    # Convert color from '255,255,255' string to (255, 255, 255) tuple
    color_tuple = tuple(map(int, color.split(',')))
    led_on(led_id, color_tuple)
    return jsonify({"message": f"LED {led_id} turned on with color {color}"}), 200

@app.route('/led/off/<int:led_id>', methods=['GET'])
def turn_led_off(led_id):
    led_off(led_id)
    return jsonify({"message": f"LED {led_id} turned off"}), 200

@app.route('/leds/on/<color>', methods=['GET'])
def turn_all_leds_on(color):
    color_tuple = tuple(map(int, color.split(',')))
    on(color_tuple)
    return jsonify({"message": "All LEDs turned on"}), 200

@app.route('/leds/off', methods=['GET'])
def turn_all_leds_off():
    off()
    return jsonify({"message": "All LEDs turned off"}), 200

@app.route('/led/display_letter/<character>/<color>', methods=['GET'])
# /led/display_letter/a/255,255,255
def api_display_letter(character, color):
    color_tuple = tuple(map(int, color.split(',')))
    display_letter(character, color_tuple)
    return jsonify({"message": f"Displayed letter {character}"}), 200

@app.route('/led/display_sentence', methods=['GET'])
def api_display_sentence():
    sentence = request.args.get('sentence')
    color = request.args.get('color', '255,255,0')  # Default to yellow if not specified
    delay = float(request.args.get('delay', 0.05))
    color_tuple = tuple(map(int, color.split(',')))
    display_sentence(sentence, color_tuple, delay)
    return jsonify({"message": f"Displayed sentence: {sentence}"}), 200

@app.route('/leds/group/<led_ids>/<color>', methods=['GET'])
def turn_group_leds_on(led_ids, color):
    led_ids_list = list(map(int, led_ids.split(',')))
    color_tuple = tuple(map(int, color.split(',')))
    for led_id in led_ids_list:
        led_on(led_id, color_tuple)
    return jsonify({"message": f"LEDs {led_ids} turned on with color {color}"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)



