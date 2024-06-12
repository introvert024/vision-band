import picamera
import pytesseract
from PIL import Image

def capture_and_ocr():
    # Capture a photo using the Raspberry Pi camera
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)  # Adjust resolution as needed
        camera.capture('photo.jpg')

    # Perform OCR on the captured image
    image_path = 'photo.jpg'
    text = perform_ocr(image_path)
    
    # Print the detected text
    print("Detected Text:")
    print(text)

def perform_ocr(image_path):
    # Use Tesseract OCR to extract text from the image
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    return text

if __name__ == "__main__":
    capture_and_ocr()
