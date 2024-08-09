import subprocess
import os
import pygame
import threading
import time
import cv2
from gtts import gTTS
from translate import Translator
from gradio_client import Client, handle_file
from face_recognition import recognize_faces

def capture_and_save_image():
    image_path = "image.jpg"

    try:
        # Capture a still image without a preview
        subprocess.run([
            "libcamera-still", 
            "-o", image_path, 
            "--nopreview",  # Option to disable preview
            "-t", "1"       # Capture duration (1 ms)
        ], check=True)
        print("Image captured and saved as 'image.jpg'.")
        return image_path
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def speak(text):
    tts = gTTS(text=text, lang='hi')
    save_path = os.path.join(os.getcwd(), "result.mp3")
    
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        
        if os.path.exists(save_path):
            os.remove(save_path)
        
        tts.save(save_path)
        
        pygame.mixer.init()
        pygame.mixer.music.load(save_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except PermissionError as e:
        print(f"PermissionError: {e}")

def process_image(client, image_path, result_event, face_recognition_event):
    try:
        result = client.predict(
            image=handle_file(image_path),
            api_name="/predict"
        )
        print("Prediction result:", result)
        result_event["result"] = result
    except Exception as e:
        print(f"Error in processing image: {e}")
    finally:
        face_recognition_event.set()

def main_loop():
    client = Client("krishnv/ImageCaptioning")
    translator = Translator(to_lang="hi")

    try:
        while True:
            image_path = capture_and_save_image()
            if image_path is not None:
                result_event = {}
                face_recognition_event = threading.Event()

                prediction_thread = threading.Thread(target=process_image, args=(client, image_path, result_event, face_recognition_event))
                prediction_thread.start()

                frame = cv2.imread(image_path)  # Read the image using OpenCV
                img, names = recognize_faces(frame)
                face_recognition_event.wait()  # Wait for face recognition to complete

                result = result_event.get("result", "")

                if "person" in result.lower():
                    result = result.lower().replace("a person", names[0] if names else "a person")
                if "man" in result.lower():
                    result = result.lower().replace("a man", names[0] if names else "a man")
                if "woman" in result.lower():
                    result = result.lower().replace("a woman", names[0] if names else "a woman")
                if "young man" in result.lower():
                    result = result.lower().replace("a young man", names[0] if names else "a young man")
                
                result = result.replace("mirror", "camera").replace("windows", "camera")
                
                translation = translator.translate(result)
                
                speak("मैं देख सकती हूँ" + translation)
                print("Recognized names:", names)
                print("Original Caption:", result)
                print("Translated Caption:", translation)
            
            time.sleep(1)  # Wait for 1 second
    finally:
        client.close()  # Clean up Gradio client

if __name__ == "__main__":
    main_loop()
