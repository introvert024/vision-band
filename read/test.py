import cv2
from gradio_client import Client, handle_file

# Step 1: Capture an image using the webcam
def capture_image(file_path='image.jpg'):
    # Initialize the camera
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        raise Exception("Could not open video device")

    # Set camera properties (optional)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Capture a single frame
    ret, frame = camera.read()

    if not ret:
        raise Exception("Failed to capture image")

    # Save the captured image
    cv2.imwrite(file_path, frame)

    # Release the camera
    camera.release()
    cv2.destroyAllWindows()

    return file_path

client = Client("krishnv/OCR-image-to-text-ZeroGPU")
result = client.predict(
		Method="PaddleOCR",
		img=handle_file('read/download.png'),
		api_name="/predict"
)
print(result)
