import cv2
import socket
import struct
import io
import numpy as np
import threading
import argparse
import time
from imutils.video import FPS
import imutils

def receive_video():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    print("Waiting for a connection from the Raspberry Pi...")

    connection, address = server_socket.accept()
    print("Connected to", address)

    connection = connection.makefile('rb')

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=True,
        help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=True,
        help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
        help="minimum probability to filter weak predictions")
    args = vars(ap.parse_args())

    CLASSES = ["aeroplane", "background", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]

    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    fps = FPS().start()

    try:
        while True:
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break

            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            image_stream.seek(0)
            frame = cv2.imdecode(np.frombuffer(image_stream.read(), dtype=np.uint8), 1)
            frame = imutils.resize(frame, width=400)

            (h, w) = frame.shape[:2]
            resized_image = cv2.resize(frame, (300, 300))
            blob = cv2.dnn.blobFromImage(resized_image, (1/127.5), (300, 300), 127.5, swapRB=True)
            net.setInput(blob)
            predictions = net.forward()

            for i in np.arange(0, predictions.shape[2]):
                confidence = predictions[0, 0, i, 2]
                if confidence > args["confidence"]:
                    idx = int(predictions[0, 0, i, 1])
                    box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    print("Object detected: ", label)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            fps.update()

    finally:
        connection.close()
        server_socket.close()

if __name__ == "__main__":
    receive_video_thread = threading.Thread(target=receive_video)
    receive_video_thread.start()

    # Give some time for the video stream to start
    time.sleep(2.0)

    receive_video_thread.join()
