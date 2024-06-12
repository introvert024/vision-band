import RPi.GPIO as GPIO
import time
import pyttsx3

TRIG = 24
ECHO = 22
GPIO.setmode(GPIO.BCM)

# Initialize the TTS engine outside the loop
engine = pyttsx3.init()

# Initialize the sensor setup once
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        print("Distance measurement in progress")
        GPIO.output(TRIG, False)
        print("Waiting for the sensor to settle")
        time.sleep(0.01)  # Adjust this settling time as needed
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Initialize variables for pulse start and end times
        pulse_start = time.time()
        pulse_end = time.time()

        # Wait for the echo response, but with a timeout
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            if (pulse_start - pulse_end) > 0.1:  # Adjust timeout as needed
                break
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            if (pulse_end - pulse_start) > 0.1:  # Adjust timeout as needed
                break

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print("Distance:", distance, "cm")

        # Convert distance to meters
        distance_in_meters = distance / 100

        # Speak the distance using TTS in meters if it's 100 centimeters or more away
        if distance_in_meters >= 1:
            # Convert to string and keep only the first decimal place
            distance_in_meters_str = "{:.1f}".format(distance_in_meters)
            engine.say(f"the object is {distance_in_meters_str} meters away")
        else:
            # Convert to string and keep only the first decimal place
            distance_str = "{:.1f}".format(distance)
            engine.say(f"the object is {distance_str} centimeters close, be careful")

        engine.runAndWait()

        time.sleep(0.5)  # Reduce the sleep time

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
