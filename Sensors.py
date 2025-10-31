#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from datetime import datetime

PIN_S1 = 22
PIN_S2 = 26
POLL_INTERVAL = 0.05
STATUS_PRINT_INTERVAL = 2.0

SENSOR1_ACTIVE_LOW = True
SENSOR2_ACTIVE_LOW = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_S1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_S2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def interpret(raw, active_low):
    if active_low:
        return (raw == 0)
    else:
        return (raw == 1)

def pretty(broken):
    return "BROKEN" if broken else "CLEAR"

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

last_state = (None, None)
last_status_print = time.time()

print("Starting sensor reader (RPi.GPIO). Ctrl-C to exit.")
try:
    while True:
        raw1 = GPIO.input(PIN_S1)  # 0 or 1
        raw2 = GPIO.input(PIN_S2)

        broken1 = interpret(raw1, SENSOR1_ACTIVE_LOW)
        broken2 = interpret(raw2, SENSOR2_ACTIVE_LOW)

        if (broken1, broken2) != last_state:
            print(f"{timestamp()}  S1: {pretty(broken1)} (raw={raw1})  |  S2: {pretty(broken2)} (raw={raw2})")
            last_state = (broken1, broken2)
            last_status_print = time.time()

        if time.time() - last_status_print >= STATUS_PRINT_INTERVAL:
            print(f"{timestamp()}  [STATUS] S1={pretty(broken1)} (raw={raw1})  S2={pretty(broken2)} (raw={raw2})")
            last_status_print = time.time()

        time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("\nExiting.")

finally:
    GPIO.cleanup()
