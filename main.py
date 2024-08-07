import subprocess
import time
import pygame
from gpiozero import Button
from threading import Timer

def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def handle_button_press(button1, button2):
    while True:
        button1.wait_for_press()
        subprocess.run(['python', 'hindi.py'])
        button1.close()  # Ensure button is released
        button2.wait_for_press()
        subprocess.run(['python', 'english.py'])
        button2.close()  # Ensure button is released

def cleanup(button1, button2):
    button1.close()
    button2.close()
    print("GPIO cleaned up. Exiting program.")

def auto_exit():
    print('Timeout reached. Exiting automatically.')
    cleanup(button1, button2)
    exit(0)

if __name__ == "__main__":
    button1 = Button(15)  # right side
    button2 = Button(27)  # left side

    # Play audio files before waiting for button press
    play_audio("hindi.mp3")
    play_audio("english.mp3")

    # Set up the timer to automatically exit after 5 seconds
    timer = Timer(5.0, auto_exit)
    timer.start()
    
    try:
        # Start waiting for button presses
        handle_button_press(button1, button2)
    except Exception as e:
        print(f"Error: {e}")
        cleanup(button1, button2)
