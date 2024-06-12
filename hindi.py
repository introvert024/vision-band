import subprocess
from gtts import gTTS
import pygame
import requests
from gpiozero import Button

# # Hindi text
# hindi_text = "नमस्ते, मेरा नाम viba है और मैं आपकी सेवा में मौजूद हूँ आपको ये दुनिया मेरी नज़रों से दिखाने के लिए।"
# # Create a gTTS object
# tts = gTTS(text=hindi_text, lang='hi')
# # Save the audio file
# tts.save("start_speech.mp3")
# print("Speech saved as hindi_speech.mp3")

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(10)  # Prevent the script from exiting immediately

def check_internet(url='http://www.google.com/', timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    except requests.RequestException:
        return False

# Paths to your audio files
start_audio = 'sound/hindi/start.wav'
internet_on_audio = 'sound/hindi/start1.mp3'
internet_off_audio = 'sound/hindi/nointernet.mp3'
button_audio = 'sound/hindi/button.mp3'

if __name__ == "__main__":
    # Play the initial start audio
    play_audio(start_audio)

    # Check the internet connection and play the appropriate audio
    if check_internet():
        play_audio(internet_on_audio)
    else:
        play_audio(internet_off_audio)
    
    # Play the button audio
    play_audio(button_audio)

    button = Button(2)
    button.wait_for_press()
    subprocess.run(['python', 'object/caption.py'])

