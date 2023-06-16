from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

connection_string = "/dev/ttyACM0"

# Connect to the Vehicle
print ('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

vehicle.mode = VehicleMode("LAND")