import time
import threading
import socket
import RPi.GPIO as GPIO
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials, db

# ====================== GPIO SETUP ======================
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

SOLENOID_PIN = 17
BUTTON_PIN = 26

GPIO.setup(SOLENOID_PIN, GPIO.OUT)
GPIO.output(SOLENOID_PIN, GPIO.LOW)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ====================== CONFIG ======================
PASSWORD = "*****"
TIMEOUT = 5

FIREBASE_KEY_PATH = "****"
DATABASE_URL = "https://**************/"

EMAIL_SENDER = "******@******"
EMAIL_PASSWORD = "********"

EMAIL_RECEIVERS = [
    "****",
    "****"
]

ACCOUNT_SID = "****"
AUTH_TOKEN = "****"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

WHATSAPP_RECEIVERS = [
    "whatsapp:+*****"
]

# ====================== FIREBASE INIT ======================
firebase_ok = False
firebase_app = None

def init_firebase():
    global firebase_ok, firebase_app
    try:
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': DATABASE_URL
        })
        firebase_ok = True
        print(" Firebase connected")
    except Exception as e:
        firebase_ok = False
        print("⚠️ Firebase offline:", e)

def firebase_reconnect_loop():
    while True:
        if not firebase_ok:
            print("🔄 Reconnecting Firebase...")
            init_firebase()
        time.sleep(5)

# ====================== EVENT SYSTEM (ANTI-BUG CORE) ======================
event_queue = []
event_lock = threading.Lock()
door_busy = False

def push_event(source):
    with event_lock:
        event_queue.append(source)

def process_events():
    global door_busy

    while True:
        if len(event_queue) == 0:
            time.sleep(0.1)
            continue

        if door_busy:
            time.sleep(0.2)
            continue

        with event_lock:
            source = event_queue.pop(0)

        door_busy = True
        activate_solenoid(source)
        door_busy = False

# ====================== SOLENOID ======================
lock = threading.Lock()

def activate_solenoid(source=""):
    with lock:
        print(f"🔓 Door opened by {source}")

        GPIO.output(SOLENOID_PIN, GPIO.HIGH)
        update_status(True)

        time.sleep(4)

        GPIO.output(SOLENOID_PIN, GPIO.LOW)
        update_status(False)

# ====================== FIREBASE ======================
last_firebase_state = False

def firebase_listener():
    global last_firebase_state

    while True:
        if not firebase_ok:
            time.sleep(2)
            continue

        try:
            data = db.reference("/door/command").get()

            if data is True and not last_firebase_state:
                last_firebase_state = True
                push_event("Firebase")

                db.reference("/door/command").set(False)

            elif data is False:
                last_firebase_state = False

        except Exception as e:
            print("⚠️ Firebase error:", e)

        time.sleep(1)

def update_status(state):
    if not firebase_ok:
        return
    try:
        db.reference("/door/status").set(state)
    except:
        pass

# ====================== ALERTS ======================
last_alert_time = 0

def send_email_alert():
    try:
        for receiver in EMAIL_RECEIVERS:
            msg = MIMEText(
                "⚠️ WRONG PIN ATTEMPT\n\n"
                "Someone tried to access the robot lab.\n\n"
                "Open link:\n"
                "******/\n\n\n"
                "mail : *****\n"
                "password : *****"
            )

            msg["Subject"] = "Security Alert"
            msg["From"] = EMAIL_SENDER
            msg["To"] = receiver

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, receiver, msg.as_string())

    except:
        print("⚠️ Email failed")

def send_whatsapp_alert():
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        for receiver in WHATSAPP_RECEIVERS:
            client.messages.create(
                body="⚠️ Wrong PIN attempt detected\nhttps://remote-door-project-2d781.web.app/\nmail: secure@gmail.com\npassword: robotiqueensi",
                from_=TWILIO_WHATSAPP_NUMBER,
                to=receiver
            )
    except:
        print("⚠️ WhatsApp failed")

def security_alert():
    global last_alert_time

    if time.time() - last_alert_time < 5:
        return

    last_alert_time = time.time()

    threading.Thread(target=send_email_alert, daemon=True).start()
    threading.Thread(target=send_whatsapp_alert, daemon=True).start()

# ====================== KEYPAD ======================
ROWS = [6, 5, 19, 13]
COLS = [21, 20, 16, 12]

KEYPAD = [
    ["1","2","3","A"],
    ["4","5","6","B"],
    ["7","8","9","C"],
    ["*","0","#","D"]
]

for r in ROWS:
    GPIO.setup(r, GPIO.OUT)
    GPIO.output(r, GPIO.LOW)

for c in COLS:
    GPIO.setup(c, GPIO.IN, pull_up_down=GPIO.PUD_UP)

entered = ""
last_input_time = None

def read_keypad():
    for i, row in enumerate(ROWS):
        GPIO.output(row, GPIO.HIGH)

        for j, col in enumerate(COLS):
            if GPIO.input(col) == GPIO.LOW:
                while GPIO.input(col) == GPIO.LOW:
                    time.sleep(0.01)
                GPIO.output(row, GPIO.LOW)
                return KEYPAD[i][j]

        GPIO.output(row, GPIO.LOW)

    return None

# ====================== MAIN ======================
print("🚪 SMART DOOR SYSTEM STABLE VERSION STARTED")

init_firebase()

threading.Thread(target=firebase_reconnect_loop, daemon=True).start()
threading.Thread(target=firebase_listener, daemon=True).start()
threading.Thread(target=process_events, daemon=True).start()

try:
    while True:
        key = read_keypad()

        # BUTTON
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            push_event("Button")
            time.sleep(0.4)

        if key:
            entered += key
            last_input_time = time.time()

        if entered and last_input_time:
            if time.time() - last_input_time > TIMEOUT:
                entered = ""

        if len(entered) == 5:
            if entered == PASSWORD:
                push_event("Keypad")
            else:
                print("❌ Wrong PIN")
                security_alert()

            entered = ""

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    GPIO.output(SOLENOID_PIN, GPIO.LOW)
    GPIO.cleanup()