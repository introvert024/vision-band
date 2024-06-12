import cv2
import pytesseract
from PIL import Image
import tempfile
import numpy as np
import matplotlib.pyplot as plt

def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.LANCZOS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

def capture_image_from_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    print("Press 'Space' to capture the image.")
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename = temp_file.name
    cv2.imwrite(temp_filename, frame)

    return temp_filename

def main():
    image_path = capture_image_from_camera()
    if image_path is None:
        return

    print(f"Image saved at {image_path}")
    image_dpi_path = set_image_dpi(image_path)
    extracted_information = pytesseract.image_to_string(Image.open(image_dpi_path))
    print("Extracted Text:")
    print(extracted_information)

    img = Image.open(image_dpi_path)
    plt.imshow(np.asarray(img))
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
