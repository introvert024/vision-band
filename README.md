# stage 1 without prompt vison band Headband by krish verma 

![Smart Blind Headband](Smart-blind-headband/WhatsApp Image 2023-11-10 at 2.47.47 PM.jpeg)

The Smart Blind Headband is an innovative wearable solution designed to enhance the navigation and interaction capabilities of visually impaired individuals. By integrating Raspberry Pi Zero, ultrasonic sensors, and a high-resolution camera, this device enables real-time obstacle detection and advanced image recognition, contributing to increased independence and safety for users.

## Features

- **Real-time Obstacle Detection:** Instantaneously identifies obstacles, providing crucial feedback to users.
- **Advanced Image Recognition:** Utilizes state-of-the-art image recognition software for precise object identification.
- **Intuitive User Interface:** Crafted for effortless interaction with audio feedback and tactile cues.

## Hardware Requirements

- Raspberry Pi 4/5
- lidar sesnor
- Pi Camera

## Getting Started

  ## installing and updating basic dependencies 
```bash
sudo apt update
sudo apt full-upgrade
```
## now install and steup virtual enviroment 
```bash
sudo apt install python3-venv
python3 -m venv env ## Run the following command to create a virtual environment. Replace env with the name you want for your virtual environment.
source env/bin/activate ## Activate the virtual environment
```
## Now install all packages in the ENV
```bash
sudo apt-get install libcblas-dev # not important 
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev # not important 
sudo apt-get install libqtgui4  # not important 
sudo apt-get install libqt4-test # not important
pip install opencv-python==4.5.3.56
pip install opencv-contrib-python
pip install opencv-python-headless
pip install opencv-contrib-python-headless
pip install matplotlib
pip install imutils
## extra -- sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test
```

 ## now object detection 
 Clone the repo and go to the object detection folder 
 ```bash
 git clone https://github.com/introvert024/Smart-blind-headband.git
 cd Smart-blind-headband/Object_detection
 ```

 ## now run the object detection 

 make sure to enable pi camera with "sudo-raspi config" 
 ```bash
 python object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
 ```
 ## List of objects it can detect currently 
 ```bash
  "aeroplane
  "background
  "bicycle
  "bird
  "boat
  "bottle
  "bus
  "car
  "cat
  "chair
  "cow
  "diningtable
  "dog
  "horse
  "motorbike
  "person
  "pottedplant
  "sheep
  "sofa
  "train
  "tvmonitor
```
