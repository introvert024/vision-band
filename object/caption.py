import cv2
from gradio_client import Client, handle_file
from gtts import gTTS
import os
import pygame
import face_recognition

def capture_and_save_image():
    # Open the default camera (usually 0 for built-in webcams)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return False

    # Capture a single frame from the camera
    ret, frame = camera.read()

    if not ret:
        print("Error: Failed to capture image.")
        camera.release()
        return False

    # Save the captured frame as an image file
    cv2.imwrite("image.jpg", frame)

    # Release the camera
    camera.release()

    print("Image captured and saved as 'image.jpg'.")
    return True

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("result.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("result.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def play_custom_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    if capture_and_save_image():
        # Now, use Gradio client to predict something based on the saved image
        client = Client("krishnv/ImageCaptioning")
        result = client.predict(
            image=handle_file('image.jpg'),
            api_name="/predict"
        )
        print("Prediction result:", result)
        
        # Check for specific keywords in the result
        keywords = ["person", "man", "woman"]
        if any(keyword in result.lower() for keyword in keywords):
            print("Keyword detected in result. Playing custom audio.")
            play_custom_audio("custom_audio.mp3")
            
            # Recognize faces and print the results
            img, names = face_recognition.recognize_faces()
            print("Recognized names:", names)
            if img is not None:
                cv2.imshow("face Detection", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        else:
            # Speak the result using gtts
            speak(result)
