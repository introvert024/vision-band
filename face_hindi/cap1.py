import os
import subprocess
import pygame
import threading
import time
from gtts import gTTS
from translate import Translator  # Add the translator import

# Import face recognition functions from face_recognition.py
from face_recognition import recognize_faces

def capture_and_save_image():
    # Define the path for the saved image
    image_path = "image.jpg"

    # Use libcamera-still to capture an image
    try:
        subprocess.run(["libcamera-still", "-o", image_path], check=True)
        print("Image captured and saved as 'image.jpg'.")
        return image_path
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def speak(text):
    tts = gTTS(text=text, lang='hi')  # Change language to Hindi
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
    translator = Translator(to_lang="hi")  # Initialize the translator

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
            
            # Translate the result to Hindi
            translation = translator.translate(result)
            
            # Speak the translated text
            speak("मैं देख सकती हूँ" + translation)
            print("Recognized names:", names)
            print("Original Caption:", result)
            print("Translated Caption:", translation)
        
        # Optionally, add a delay between iterations to avoid capturing images too rapidly
        time.sleep(1)  # Wait for 1 second (1000 milliseconds)

if __name__ == "__main__":
    main_loop()
