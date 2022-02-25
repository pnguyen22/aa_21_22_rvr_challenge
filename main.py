import board
import busio
import time
import math

from sphero_rvr import RVRDrive
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP10, echo_pin=board.GP11)

rvr = RVRDrive(uart = busio.UART(board.GP4, board.GP5, baudrate=115200))
time.sleep(0.5)

rvr.set_all_leds(255,0,0) #set leds to red
time.sleep(0.1)
rvr.set_all_leds(0,255,0) #set leds to green
time.sleep(0.1)
rvr.set_all_leds(0,0,255) #set leds to blue
time.sleep(0.1) #turn off
rvr.set_all_leds(255,255,255) #turn off leds or make them all black

rvr.sensor_start()

print("starting up")
setpoint = 60.0
k = 2
MAX_SPEED = 100

rvr.update_sensors()

sensor_distance = sonar.distance
print(sensor_distance)
error = 100
start_time = time.monotonic()
elapsed_time = time.monotonic() - start_time

#on off control
while(elapsed_time < 5.0):

    elapsed_time = time.monotonic() - start_time
    try:
        sensor_distance = sonar.distance

        # Add your proportional control code here.
        error = sensor_distance - setpoint

        output = error*k

        rvr.setMotors(output, output) #set the power of the motors for both the left and right track
            # Read the Sphero RVR library file to find the rvr.setMotors(left,right) command.
            # Use this command in the next line to send the output of your proportional
            # control to both the left and right motors.

    except RuntimeError:
        print("Retrying!")
        pass
    time.sleep(0.2)

X = rvr.get_x()
Y = rvr.get_y()

rvr.drive_to_position_si(90,X+60,Y,0.5)

# Drive for two seconds at a heading of 30 degrees


# Drive back to the starting point
# rvr.drive_to_position_si(0,0,0,0.4)
# time.sleep(3.0)
