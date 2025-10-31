#!/usr/bin/env python3
"""
read_sensors_gpiozero.py
Reads two NPN open-collector photoelectric sensors through optocoupler modules.
Uses internal pull-ups on the Pi GPIO. Polls and prints state changes and periodic status.

Wiring (BCM):
 - Sensor 1 -> opto -> GPIO 22
 - Sensor 2 -> opto -> GPIO 26

Adjust SENSOR_ACTIVE_LOW depending on how your sensor/opto behaves:
 - True  => the sensor/opto pulls the line LOW when the beam is BROKEN (common case)
 - False => the sensor/opto drives HIGH when the beam is BROKEN
"""

import time
from datetime import datetime

try:
    from gpiozero import DigitalInputDevice
except Exception as e:
    print("gpiozero import failed:", e)
    raise SystemExit("Install gpiozero (`sudo apt install python3-gpiozero`) and try again.")

# --- CONFIG ---
PIN_S1 = 22   # BCM
PIN_S2 = 26   # BCM

POLL_INTERVAL = 0.05   # seconds between polls (50 ms)
STATUS_PRINT_INTERVAL = 2.0  # seconds, periodic status print if no changes

# Set according to real behavior after you test once:
# True  -> sensor/opto pulls the Pi input to GND when the beam is BROKEN (active-low)
# False -> pulls HIGH when beam broken (active-high)
SENSOR1_ACTIVE_LOW = True
SENSOR2_ACTIVE_LOW = True
# --------------


s1 = DigitalInputDevice(PIN_S1, pull_up=True)  # value: 1 when high, 0 when low
s2 = DigitalInputDevice(PIN_S2, pull_up=True)

def interpret(value, active_low):
    """Return True if beam is BROKEN, False if CLEAR."""
    # value: 1 (HIGH) or 0 (LOW)
    if active_low:
        return (value == 0)   # LOW -> broken
    else:
        return (value == 1)   # HIGH -> broken

def pretty(broken):
    return "BROKEN" if broken else "CLEAR"

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

last_state = (None, None)
last_status_print = time.time()

print("Starting sensor reader (gpiozero). Ctrl-C to exit.")
print(f"Sensor pins: S1=GPIO{PIN_S1}, S2=GPIO{PIN_S2}")
print("Using internal pull-ups. Adjust SENSOR?_ACTIVE_LOW if logic is inverted after testing.\n")

try:
    while True:
        raw1 = int(s1.value)   # 0 or 1
        raw2 = int(s2.value)

        broken1 = interpret(raw1, SENSOR1_ACTIVE_LOW)
        broken2 = interpret(raw2, SENSOR2_ACTIVE_LOW)

        if (broken1, broken2) != last_state:
            print(f"{timestamp()}  S1: {pretty(broken1)} (raw={raw1})  |  S2: {pretty(broken2)} (raw={raw2})")
            last_state = (broken1, broken2)
            last_status_print = time.time()

        # periodic status print if no change for a while
        if time.time() - last_status_print >= STATUS_PRINT_INTERVAL:
            print(f"{timestamp()}  [STATUS] S1={pretty(broken1)} (raw={raw1})  S2={pretty(broken2)} (raw={raw2})")
            last_status_print = time.time()

        time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("\nExiting.")
