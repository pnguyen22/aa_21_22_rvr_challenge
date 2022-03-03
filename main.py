# Write your code here :-)
# sonar example 2022-02-21
import board, busio, time, math, digitalio, adafruit_hcsr04
from ssis_rvr   import pin
from sphero_rvr import RVRDrive

rvr   = RVRDrive(uart = busio.UART(pin.TX, pin.RX, baudrate=115200))
sonar = adafruit_hcsr04.HCSR04(trigger_pin=pin.TRIGGER, echo_pin=pin.ECHO)

print("starting up")

MAX_SPEED = 100


error = 100
start_time = time.monotonic()
elapsed_time = time.monotonic() - start_time

rvr.reset_yaw()
rvr.sensor_start()
#on off control

setpoint = 10.0
k = 1
while(elapsed_time < 5.0):

    elapsed_time = time.monotonic() - start_time
    try:
        sensor_distance = sonar.distance
        print(sensor_distance)
 # Add your proportional control code here.
        error = sensor_distance - setpoint
        if(error<3 and error >-3):
            break

        output = error*k

        rvr.setMotors(output, output) #set the power of the motors for both the left and right track
            # Read the Sphero RVR library file to find the rvr.setMotors(left,right) command.
            # Use this command in the next line to send the output of your proportional
            # control to both the left and right motors.

    except RuntimeError:
        print("Retrying")
        pass
    time.sleep(0.2)
    
start_time = time.monotonic()
elapsed_time = 0
rvr.update_sensors()
X = rvr.get_x()
#setpoint is 60 to the right(in the x direction) from the current position
setpoint = X+0.60
k = 100
while(elapsed_time < 5.0):
    elapsed_time = time.monotonic() - start_time
    rvr.update_sensors()
    X = rvr.get_x()
    error = setpoint-X
    output = k * error
    rvr.drive(output,90)
    time.sleep(0.2)
    if(setpoint-X<0.03):
        break

start_time = time.monotonic()
elapsed_time = 0
rvr.update_sensors()
X = rvr.get_x()
#setpoint is 60 to the right(in the x direction) from the current position
setpoint = X+0.60
k = 100
while(elapsed_time < 5.0):
    elapsed_time = time.monotonic() - start_time
    rvr.update_sensors()
    X = rvr.get_x()
    error = setpoint-X
    output = k * error
    rvr.drive(output,45)
    time.sleep(0.2)
    if(setpoint-X<0.03):
        break
