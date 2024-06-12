import subprocess
import time
import pygame
from gpiozero import Button

def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def handle_button_press():
    button_press_count = 0  # Initialize button press count
    button = Button(2)  # Assuming button is connected to GPIO pin 2
    
    while True:
        button.wait_for_press()
        button_press_count += 1
        
        if button_press_count == 1:
            subprocess.run(['python', 'hindi.py'])
        elif button_press_count == 2:
            subprocess.run(['python', 'english.py'])
        
        # Reset button press count after a short delay
        time.sleep(0.2)
        button_press_count = 0

if __name__ == "__main__":
    # Play audio files before waiting for button press
    play_audio("hindi.mp3")
    play_audio("english.mp3")
    
    # Start waiting for button presses
    handle_button_press()
