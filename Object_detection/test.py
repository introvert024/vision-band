from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import RPi.GPIO as GPIO
import pyttsx3

# Argument parsing for object detection
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
    help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
    help="minimum probability to filter weak predictions")
args = vars(ap.parse_args())

CLASSES = ["aeroplane", "background", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

fps = FPS().start()

# GPIO setup for distance measurement
TRIG = 24
ECHO = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Initialize the TTS engine outside the loop
engine = pyttsx3.init()

# Function to measure dista
def measure_distance():
    GPIO.output(TRIG, False)
    print("Waiting for the sensor to settle")
    time.sleep(0.01)  # Adjust this settling time as needed

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

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

    # Convert distance to meters
    distance_in_meters = distance / 100

    return distance_in_meters


try:
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        (h, w) = frame.shape[:2]
        resized_image = cv2.resize(frame, (300, 300))
        blob = cv2.dnn.blobFromImage(resized_image, (1/127.5), (300, 300), 127.5, swapRB=True)
        net.setInput(blob)
        predictions = net.forward()

        # Object detection loop
        for i in np.arange(0, predictions.shape[2]):
            confidence = predictions[0, 0, i, 2]
            if confidence > args["confidence"]:
                idx = int(predictions[0, 0, i, 1])
                box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                print("Object detected: ", label)

                # Get the average distance from the sensor
                distance = measure_distance()

                # Speak out the detected object and distance
                distance_unit = "meters" if distance >= 1 else "centimeters"
                output_text = f"The {CLASSES[idx]} is {distance} {distance_unit} away"
                print(output_text)
                engine.say(output_text)
                engine.runAndWait()

                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        #cv2.imshow("Frame", frame)
       # key = cv2.waitKey(1) & 0xFF
       # if key == ord("q"):
      #      break
 #       fps.update()
except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
    fps.stop()
    vs.stop()
# Clean up
#cv2.destroyAllWindows()


