import io
import picamera
import socket
import struct
import time

def send_video():
    client_socket = socket.socket()
    client_socket.connect(('YOUR_COMPUTER_IP', 8000))  # Replace 'YOUR_COMPUTER_IP' with your computer's IP address

    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)  # Adjust the resolution as needed
            camera.framerate = 24

            time.sleep(2)  # Allow the camera to warm up

            start = time.time()
            stream = io.BytesIO()

            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                stream.seek(0)
                stream.truncate()

                # Receive object detection result from the computer
                object_detected = client_socket.recv(1024).decode()
                print("Object Detected on Computer:", object_detected)

    finally:
        connection.close()
        client_socket.close()

if __name__ == "__main__":
    send_video()
