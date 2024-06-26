import cv2
import numpy as np

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    names = []

    for (x,y,w,h) in features:
        cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)
         
        id, pred = clf.predict(gray_img[y:y+h,x:x+w])
        confidence = int(100*(1-pred/300))
         
        if confidence > 70:
            if id == 1:
                name = "Krish"
            elif id == 2:
                name = "Aditya"
            else:
                name = "UNKNOWN"
        else:
            name = "UNKNOWN"

        names.append(name)
        cv2.putText(img, name, (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
     
    return img, names

def recognize_faces(image):
    # loading classifier
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    if image is not None:
        img, names = draw_boundary(image, faceCascade, 1.3, 6, (255,255,255), "Face", clf)
        return img, names
    else:
        return None, []

if __name__ == "__main__":
    # Test with an example image
    image = cv2.imread("image.jpg")
    img, names = recognize_faces(image)
    print("Recognized names:", names)
    if img is not None:
        cv2.imshow("face Detection", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
