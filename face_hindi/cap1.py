import subprocess
import os
import pygame
import threading
import time
from gtts import gTTS
from translate import Translator
from gradio_client import Client, handle_file
from face_recognition import recognize_faces

def capture_and_save_image():
    image_path = "image.jpg"

    try:
        # Capture a still image with no preview
        subprocess.run([
            "libcamera-vid", 
            "-t", "1",  # Duration of the recording (1 ms, essentially capturing a single frame)
            "--no-preview", 
            "-o", image_path
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
    result = client.predict(
        image=handle_file(image_path),
        api_name="/predict"
    )
    print("Prediction result:", result)
    result_event["result"] = result
    face_recognition_event.set()

def main_loop():
    client = Client("krishnv/ImageCaptioning")
    translator = Translator(to_lang="hi")

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

if __name__ == "__main__":
    main_loop()
