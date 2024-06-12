import cv2
from gradio_client import Client, handle_file
from gtts import gTTS
import os
import pygame

def capture_and_save_image():
    # Open the default camera (usually 0 for built-in webcams)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame from the camera
    ret, frame = camera.read()

    if not ret:
        print("Error: Failed to capture image.")
        camera.release()
        return

    # Save the captured frame as an image file
    cv2.imwrite("image.jpg", frame)

    # Release the camera
    camera.release()

    print("Image captured and saved as 'image.jpg'.")

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("result.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("result.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    capture_and_save_image()

    # Now, use Gradio client to predict something based on the saved image
    client = Client("krishnv/ImageCaptioning")
    result = client.predict(
        image=handle_file('image.jpg'),
        api_name="/predict"
    )
    print(result)
    
    # Speak the result using gtts
    speak(result)
