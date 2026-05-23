# Secure-Entry Smart Door System

Secure-Entry is a Raspberry Pi based access control system that combines keypad PIN entry, face recognition, and remote control through Firebase. It drives a solenoid lock and sends alerts for wrong PIN attempts.

## Features

- Keypad PIN unlock
- Face recognition using OpenCV LBPH
- Remote open via Firebase Realtime Database
- Email and WhatsApp alerts on wrong PIN
- Solenoid lock control with a push button

## Project Structure

- `main.py` - Main door controller (GPIO, keypad, Firebase, alerts)
- `save.py` - Capture face images for a person
- `augment.py` - Data augmentation for faces
- `train.py` - Train LBPH model and save labels
- `detect_face.py` - Live face detection and recognition
- `images/` - Wiring and build photos
- `demo.mp4` - Project demo video

## Hardware

- Raspberry Pi (tested with Zero 2 W)
- Camera module or USB camera
- 4x4 keypad
- Push button
- Solenoid lock + 12V power supply
- NPN transistor (TIP120 or similar) and flyback diode
- Wires, resistors, and common ground

## Wiring Notes

- Solenoid lock is driven through a transistor with a flyback diode and separate 12V supply.
- Share ground between the Raspberry Pi and the 12V supply.
- GPIO pins in `main.py`:
  - Solenoid: GPIO 17
  - Button: GPIO 26
  - Keypad rows: GPIO 6, 5, 19, 13
  - Keypad cols: GPIO 21, 20, 16, 12

## Software Requirements

- Python 3.9+
- OpenCV with contrib modules (required for `cv2.face`)
- numpy
- firebase-admin
- twilio
- RPi.GPIO (Raspberry Pi only)

Install dependencies (on Raspberry Pi):

```bash
python -m pip install opencv-contrib-python numpy firebase-admin twilio RPi.GPIO
```

## Setup

1. Create a dataset folder:
   - `known_faces/<person_name>/` with images inside.
2. Configure secrets in `main.py`:
   - `PASSWORD`, Firebase key path and URL
   - Email sender and password
   - Twilio account settings
3. Make sure the Haar cascade file can be downloaded (the scripts will fetch it if missing).

## Usage

### 1) Capture faces

```bash
python save.py
```

### 2) Augment images (optional)

```bash
python augment.py
```

### 3) Train model

```bash
python train.py
```

### 4) Test live recognition

```bash
python detect_face.py
```

### 5) Run the full door system

```bash
python main.py
```

### 6) Test keypad only
## Media

Demo video : https://drive.google.com/drive/folders/1_1uyPSZ0tulJLGlMxORozhvnuZMWxBsU \n
rapport : https://drive.google.com/drive/folders/1nSCV6HwBXUD6e2LcyMuNfCZ53oxWeRsh
```



Build photo:

![Door build](images/555f2f78-0d71-4f76-a9bc-bf39b1ace30f.png)

Wiring diagram:

![Wiring diagram](images/625759319_1415197293593456_7040423243210406227_n.png)

Raspberry Pi pinout:

![Pi pinout](images/67aa3834-6482-4ecc-9e2d-e4ad3837cbbe.jpg)

## Troubleshooting

- If `cv2.face` is missing, install `opencv-contrib-python` instead of `opencv-python`.
- If the camera does not open, adjust the backend in `detect_face.py` and `save.py`.
- GPIO access may require running with `sudo` on Raspberry Pi.

## Safety

This project controls a real door lock. Test with power disconnected first, and ensure wiring is correct before applying 12V power.
