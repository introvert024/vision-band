import cv2
from gradio_client import Client, handle_file
from gtts import gTTS
import os
import pygame
import threading
import time

# Import face recognition functions from face_recognition.py
from face_recognition import recognize_faces

def capture_and_save_image():
    # Open the default camera (usually 0 for built-in webcams)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return None

    # Capture a single frame from the camera
    ret, frame = camera.read()

    if not ret:
        print("Error: Failed to capture image.")
        camera.release()
        return None

    # Save the captured frame as an image file
    cv2.imwrite("image.jpg", frame)

    # Release the camera
    camera.release()

    print("Image captured and saved as 'image.jpg'.")
    return frame

def speak(text):
    tts = gTTS(text=text, lang='en')
    save_path = os.path.join(os.getcwd(), "result.mp3")
    
    try:
        # Ensure pygame mixer is properly initialized and stopped
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        
        # Remove the existing file if it exists
        if os.path.exists(save_path):
            os.remove(save_path)
        
        # Save the new TTS output to result.mp3
        tts.save(save_path)
        
        # Initialize pygame mixer and play the new result.mp3
        pygame.mixer.init()
        pygame.mixer.music.load(save_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except PermissionError as e:
        print(f"PermissionError: {e}")

def process_image(client, frame, result_event, face_recognition_event):
    result = client.predict(
        image=handle_file('image.jpg'),
        api_name="/predict"
    )
    print("Prediction result:", result)
    result_event["result"] = result

    face_recognition_event.set()

def main_loop():
    client = Client("krishnv/ImageCaptioning")

    while True:
        frame = capture_and_save_image()
        if frame is not None:
            result_event = {}
            face_recognition_event = threading.Event()

            prediction_thread = threading.Thread(target=process_image, args=(client, frame, result_event, face_recognition_event))
            prediction_thread.start()

            img, names = recognize_faces(frame)
            face_recognition_event.wait()  # Wait for face recognition to complete

            result = result_event.get("result", "")

            # Replace keywords with recognized names or "KNOWN FACE"
            if "person" in result.lower():
                result = result.lower().replace("a person", names[0] if names else "a person")
            if "man" in result.lower():
                result = result.lower().replace("a man", names[0] if names else "a man")
            if "woman" in result.lower():
                result = result.lower().replace("a woman", names[0] if names else "a woman")
            if "young man" in result.lower():
                result = result.lower().replace("a young man", names[0] if names else "a young man")
            
            # Replace "mirror" and "windows" with "camera"
            result = result.replace("mirror", "camera").replace("windows", "camera")
            
            speak("I can see " + result)
            print("Recognized names:", names)
        
        # Optionally, add a delay between iterations to avoid capturing images too rapidly
        time.sleep(1)  # Wait for 1 second (1000 milliseconds)

if __name__ == "__main__":
    main_loop()
