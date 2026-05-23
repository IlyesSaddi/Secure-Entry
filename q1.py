import RPi.GPIO as GPIO
import time

# ===== GPIO setup =====
GPIO.setmode(GPIO.BCM)

# Rows and columns (your wiring)
# Top row = 1 2 3 A
ROWS = [6,5,19, 13]   # flip rows to match top-to-bottom
COLS = [21,20,16,12] # keep columns left-to-right# Keypad layout
KEYPAD = [
    ["1","2","3","A"],
    ["4","5","6","B"],
    ["7","8","9","C"],
    ["*","0","#","D"]
]

# Setup rows as outputs, columns as inputs with pull-ups
for row in ROWS:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.LOW)

for col in COLS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ===== Function to read keypad =====
def read_keypad():
    for i, row in enumerate(ROWS):
        GPIO.output(row, GPIO.HIGH)
        for j, col in enumerate(COLS):
            if GPIO.input(col) == GPIO.LOW:
                while GPIO.input(col) == GPIO.LOW:
                    time.sleep(0.01)  # wait for key release
                GPIO.output(row, GPIO.LOW)
                return KEYPAD[i][j]
        GPIO.output(row, GPIO.LOW)
    return None

# ===== Main loop =====
try:
    print("Keypad ready. Press keys:")
    while True:
        key = read_keypad()
        if key:
            print("Pressed:", key)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()






