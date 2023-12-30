from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import pytesseract
import pyttsx3

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 180
camera.sharpness = 60
rawCapture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warm up
time.sleep(0.1)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    # Use Tesseract to extract text from the image
    text = pytesseract.image_to_string(image)

    # Speak the recognized text
    engine.say(text)
    engine.runAndWait()

    print(text)

    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break

