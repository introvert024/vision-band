# import packages
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak predictions")
args = vars(ap.parse_args())

# load our serialized model
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# load the input image and grab its dimensions
image = cv2.imread(args["image"])
(h, w) = image.shape[:2]

# prepare the image for object detection
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), (1/127.5), (300, 300), 127.5, swapRB=True)
net.setInput(blob)
predictions = net.forward()

# loop over the predictions
for i in np.arange(0, predictions.shape[2]):
    confidence = predictions[0, 0, i, 2]
    if confidence > args["confidence"]:
        idx = int(predictions[0, 0, i, 1])
        box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
        print("Object detected: ", label)

# Release resources
cv2.destroyAllWindows()
