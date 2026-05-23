Secure-Entry Smart Door System

Secure-Entry is a Raspberry Pi-based access control system that combines keypad PIN authentication, face recognition, and remote control through Firebase. The system controls a solenoid door lock and sends alerts when unauthorized access attempts are detected.

Features
PIN-based door unlocking using a 4x4 keypad
Face recognition using OpenCV LBPH
Remote door opening through Firebase Realtime Database
Email and WhatsApp notifications for incorrect PIN attempts
Solenoid lock control with a physical push button
Local and remote access management
Project Structure
main.py – Main door controller (GPIO, keypad, Firebase, notifications)
save.py – Capture face images for a user
augment.py – Perform face image augmentation
train.py – Train the LBPH face recognition model and save labels
detect_face.py – Real-time face detection and recognition
images/ – Hardware wiring and assembly photos
demo.mp4 – Demonstration video
Hardware Requirements
Raspberry Pi (tested on Raspberry Pi Zero 2 W)
Raspberry Pi Camera Module or USB Camera
4x4 Matrix Keypad
Push Button
Solenoid Door Lock
12V Power Supply
NPN Transistor (TIP120 or equivalent)
Flyback Diode (1N4007 or equivalent)
Jumper Wires and Resistors
Wiring Notes
The solenoid lock is driven through an NPN transistor with a flyback diode for protection.
Use a separate 12V power supply for the solenoid lock.
Connect the grounds of the Raspberry Pi and the 12V power supply together.
GPIO Configuration (main.py)
Component	GPIO Pin
Solenoid Lock	GPIO 17
Push Button	GPIO 26
Keypad Rows	GPIO 6, 5, 19, 13
Keypad Columns	GPIO 21, 20, 16, 12
Software Requirements
Python 3.9+
OpenCV Contrib (required for cv2.face)
NumPy
Firebase Admin SDK
Twilio
RPi.GPIO (Raspberry Pi only)
Installation
python -m pip install opencv-contrib-python numpy firebase-admin twilio RPi.GPIO
Setup
1. Create the Face Dataset

Create the following directory structure:

known_faces/
└── person_name/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
2. Configure Credentials

Update the following parameters in main.py:

PASSWORD
Firebase service account key path
Firebase database URL
Email sender address and password
Twilio Account SID, Auth Token, and phone numbers
3. Haar Cascade

The required Haar Cascade file will be automatically downloaded if it is not already available.

Usage
Capture Face Images
python save.py
Augment Dataset (Optional)
python augment.py
Train the Recognition Model
python train.py
Test Live Face Recognition
python detect_face.py
Run the Complete Door Access System
python main.py
Media
Demo Video

https://drive.google.com/drive/folders/1_1uyPSZ0tulJLGlMxORozhvnuZMWxBsU

Project Report

https://drive.google.com/drive/folders/1nSCV6HwBXUD6e2LcyMuNfCZ53oxWeRsh

Images
Door Prototype
images/555f2f78-0d71-4f76-a9bc-bf39b1ace30f.png
Wiring Diagram
images/625759319_1415197293593456_7040423243210406227_n.png
Raspberry Pi Pinout
images/67aa3834-6482-4ecc-9e2d-e4ad3837cbbe.jpg
Troubleshooting
cv2.face Module Not Found

Install the OpenCV Contrib package instead of the standard OpenCV package:

pip uninstall opencv-python
pip install opencv-contrib-python
Camera Cannot Be Opened
Verify that the camera is connected correctly.
Check camera permissions.
Try a different OpenCV backend in detect_face.py and save.py.
GPIO Permission Errors

Run the application with elevated privileges:

sudo python main.py
Security and Safety

 This project controls a physical door lock.

Before connecting the 12V supply:

Verify all wiring connections carefully.
Test the circuit without the lock connected.
Ensure the flyback diode is installed correctly.
Confirm that the transistor and power supply are rated for the lock current.

Improper wiring may damage the Raspberry Pi, power supply, or lock mechanism.

Future Improvements
Mobile application for remote monitoring
Face recognition using deep learning models
Visitor management system
Event logging and access history
Multi-user authentication levels
Video intercom integration
