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
    button1 = Button(2)  # Assuming button 1 is connected to GPIO pin 2
    button2 = Button(3)  # Assuming button 2 is connected to GPIO pin 3
    
    while True:
        button1.wait_for_press()
        subprocess.run(['python', 'hindi.py'])
        
        button2.wait_for_press()
        subprocess.run(['python', 'english.py'])

if __name__ == "__main__":
    # Play audio files before waiting for button press
    play_audio("hindi.mp3")
    play_audio("english.mp3")
    
    # Start waiting for button presses
    handle_button_press()
