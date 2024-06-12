# VIBA: The Ultimate IoT Solution for the Visually Impaired

Welcome to the official repository of **VIBA** - an innovative IoT solution designed to assist visually impaired individuals by leveraging cutting-edge technology such as GPS, distance calculation, object reading, image capturing, advanced video capturing, and face recognition.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
   - [GPS Navigation](#gps-navigation)
   - [Distance Calculation](#distance-calculation)
   - [Object Reading](#object-reading)
   - [Image Capturing](#image-capturing)
   - [Advanced Video Capturing](#advanced-video-capturing)
   - [Face Recognition](#face-recognition)
3. [Installation](#installation)
4. [Usage](#usage)
   - [GPS Navigation](#using-gps-navigation)
   - [Distance Calculation](#using-distance-calculation)
   - [Object Reading](#using-object-reading)
   - [Image Capturing](#using-image-capturing)
   - [Advanced Video Capturing](#using-advanced-video-capturing)
   - [Face Recognition](#using-face-recognition)
5. [Architecture](#architecture)
   - [Hardware Components](#hardware-components)
   - [Software Components](#software-components)
6. [API Documentation](#api-documentation)
7. [Contributing](#contributing)
8. [License](#license)
9. [Acknowledgements](#acknowledgements)

---

## Introduction

**VIBA** (Visually Impaired Body Assistant) is a comprehensive IoT solution aimed at providing enhanced assistance to visually impaired individuals. By integrating various advanced technologies, VIBA serves as an all-in-one assistant that aids navigation, object detection, face recognition, and much more.

The core objective of VIBA is to empower visually impaired people to navigate their environment more safely and independently. Whether it’s finding the best route to a destination, identifying objects and faces, or capturing images and videos for later analysis, VIBA offers a suite of functionalities that significantly improve the quality of life for its users.

---

## Features

### GPS Navigation

VIBA’s GPS navigation feature provides real-time guidance to users, helping them reach their destinations efficiently and safely. By using GPS data, the device can determine the user’s current location and provide audio instructions for navigating to a specified destination.

- Real-time location tracking
- Audio navigation instructions
- Route optimization
- Support for multiple languages

### Distance Calculation

The distance calculation feature enables VIBA to measure the distance to various objects or landmarks. This feature is particularly useful for helping users maintain a safe distance from obstacles and navigate through unfamiliar environments.

- Real-time distance measurement
- Audio feedback on distance
- Obstacle detection
- Integration with GPS for enhanced navigation

### Object Reading

VIBA is equipped with advanced object recognition capabilities. By utilizing computer vision and machine learning algorithms, the device can identify and describe objects in the user’s vicinity.

- Real-time object detection
- Audio descriptions of identified objects
- Support for a wide range of object categories
- Continuous learning for improved accuracy

### Image Capturing

The image capturing feature allows users to take pictures of their surroundings. These images can be stored for later reference or analyzed by VIBA to provide detailed descriptions of the scene.

- High-resolution image capture
- Audio feedback on captured images
- Storage and management of captured images
- Integration with object reading for scene analysis

### Advanced Video Capturing

In addition to images, VIBA can also capture high-definition video. This feature is useful for recording events or capturing detailed visual information that can be analyzed later.

- High-definition video recording
- Audio commentary on recorded videos
- Storage and management of video files
- Integration with face recognition for enhanced analysis

### Face Recognition

The face recognition feature enables VIBA to identify and recognize faces of people in the user’s environment. This can be particularly helpful for social interactions and ensuring the user knows who is around them.

- Real-time face detection and recognition
- Audio identification of recognized individuals
- Storage of known faces for future reference
- Continuous learning for improved recognition accuracy

---

## Installation

To get started with VIBA, follow the steps below to install the necessary software and configure the hardware components.

### Prerequisites

Ensure you have the following prerequisites installed on your system:

- Python 3.7 or higher
- OpenCV
- TensorFlow
- PyTorch
- GPS module drivers
- Camera module drivers

### Installation Steps

1. Clone the VIBA repository from GitHub:

```bash
git clone https://github.com/yourusername/VIBA.git
cd VIBA
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Configure the GPS and camera modules according to the hardware setup guide provided in the `docs/hardware_setup.md`.

4. Run the initial setup script to configure VIBA:

```bash
python setup.py
```

---

## Usage

Once VIBA is installed and configured, you can start using its various features. Below are detailed instructions on how to use each feature.

### Using GPS Navigation

1. Launch the GPS navigation module:

```bash
python viba/gps_navigation.py
```

2. Follow the audio instructions to set your destination.

3. VIBA will provide real-time audio guidance to help you reach your destination.

### Using Distance Calculation

1. Launch the distance calculation module:

```bash
python viba/distance_calculation.py
```

2. The device will continuously measure and report the distance to nearby objects.

### Using Object Reading

1. Launch the object reading module:

```bash
python viba/object_reading.py
```

2. Point the camera towards the objects you want to identify.

3. VIBA will provide audio descriptions of the identified objects.

### Using Image Capturing

1. Launch the image capturing module:

```bash
python viba/image_capturing.py
```

2. Press the capture button to take a picture.

3. The device will provide audio feedback on the captured image.

### Using Advanced Video Capturing

1. Launch the advanced video capturing module:

```bash
python viba/video_capturing.py
```

2. Press the record button to start recording a video.

3. Press the stop button to stop recording and save the video file.

### Using Face Recognition

1. Launch the face recognition module:

```bash
python viba/face_recognition.py
```

2. The device will continuously scan for faces and provide audio identification of recognized individuals.

---

## Architecture

The architecture of VIBA comprises both hardware and software components, designed to work seamlessly together to provide a comprehensive solution for the visually impaired.

### Hardware Components

- **GPS Module**: Used for real-time location tracking and navigation.
- **Camera Module**: Used for capturing images and videos, as well as for object reading and face recognition.
- **Microcontroller**: Acts as the central processing unit, coordinating all hardware components and running the software modules.
- **Speaker**: Provides audio feedback and instructions to the user.
- **Battery**: Powers the device, ensuring portability and usability on the go.

### Software Components

- **GPS Navigation Module**: Handles real-time location tracking and navigation instructions.
- **Distance Calculation Module**: Measures distances to objects and provides audio feedback.
- **Object Reading Module**: Identifies and describes objects in the user’s environment.
- **Image Capturing Module**: Captures and manages images.
- **Advanced Video Capturing Module**: Records and manages video files.
- **Face Recognition Module**: Detects and recognizes faces in real-time.

---

## API Documentation

VIBA provides a custom experience developers to extend and customize its functionalities. Below is an overview of the available APIs.

### GPS Navigation API

- `get_current_location`: Returns the current GPS coordinates.
- `get_navigation_instructions()`: Returns the next set of navigation instructions.

### Distance Calculation (hardware)

- `distance_to_object`: Use the advance ultra sonic water sensor 
### Book Reading API

- `Pytesseract`: Identifies text in the given image.

### Image Captioning API

- `Hugging face model`: model running on hugging face


### Face Recognition API

- The API is private and used under certain conditions 

---

## Contributing

We welcome contributions from the community to help improve VIBA. If you are interested in contributing, please follow the guidelines below:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Create a pull request and provide a detailed description of your changes.

Please ensure your code adheres to our coding standards and includes appropriate tests.

---

## License

VIBA is released under the MIT License. See the `LICENSE` file for more details.

---

## Acknowledgements

We would like to thank the following organizations and individuals for their support and contributions to the development of VIBA:

-

 [OpenCV](https://opencv.org/): For providing an open-source computer vision library.
- [PyTorch](https://pytorch.org/): For providing an easy-to-use deep learning framework.
- The visually impaired community: For providing valuable feedback and insights.

---

Thank you for choosing VIBA. We hope this project makes a positive impact on the lives of visually impaired individuals. If you have any questions or need further assistance, please feel free to reach out to us.
