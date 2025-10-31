from gpiozero import Button
from signal import pause

# Use BCM numbering
sensor1 = Button(22, pull_up=True)
sensor2 = Button(26, pull_up=True)

def s1_triggered():
    print("Sensor 1 beam broken!")

def s1_cleared():
    print("Sensor 1 beam clear!")

def s2_triggered():
    print("Sensor 2 beam broken!")

def s2_cleared():
    print("Sensor 2 beam clear!")

sensor1.when_pressed = s1_triggered
sensor1.when_released = s1_cleared

sensor2.when_pressed = s2_triggered
sensor2.when_released = s2_cleared

print("Watching sensors... press Ctrl+C to exit.")
pause()
