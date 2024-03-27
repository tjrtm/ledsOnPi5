import cv2
import time
import lib.neopixel_spidev as np

# Initialize LED strip
LED_COUNT = 79
pixels = np.NeoPixelSpiDev(0, 0, n=LED_COUNT, pixel_order=np.GRB)

# Keep track of the current brightness level globally
current_brightness = 0.0

def calculate_distance(face_width, focal_length, actual_width):
    return (actual_width * focal_length) / face_width

def scale_color(color, brightness_factor):
    return tuple(min(255, max(0, round(component * brightness_factor))) for component in color)

def update_leds_with_brightness(target_distance):
    global current_brightness
    min_distance = 20
    max_distance = 150
    target_brightness = max(0.0, min(1.0, 1 - (target_distance - min_distance) / (max_distance - min_distance)))
    target_brightness = round(target_brightness, 1)

    steps = 10  # Number of steps for the transition
    step_delay = 0.02  # Delay between steps in seconds

    # Calculate step size for a smooth transition
    brightness_step = (target_brightness - current_brightness) / steps

    # Gradually update brightness in steps
    for _ in range(steps):
        current_brightness += brightness_step
        scaled_color = scale_color((255, 255, 255), current_brightness)
        pixels.fill(scaled_color)
        pixels.brightness = (current_brightness)
        pixels.show()
        time.sleep(step_delay)
    
    # Ensure final brightness is set to the target brightness
    current_brightness = target_brightness

# Face detection setup
cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)
cap = cv2.VideoCapture(0)
actual_width = 15.0  
focal_length = 300  # Calibration here
try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.resize(frame, (800, 600), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            largest_face = max(faces, key=lambda face: face[2] * face[3])
            distance = calculate_distance(largest_face[2], focal_length, actual_width)
            update_leds_with_brightness(distance)

        time.sleep(0.1)  

finally:
    cap.release()
    cv2.destroyAllWindows()
    pixels.fill((0, 0, 0))
    pixels.show()
