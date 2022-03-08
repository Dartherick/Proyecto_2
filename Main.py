import dronekit
import time

#Connects to the vehicle using serial port.
Drone = dronekit.connect('/dev/ttyS0', wait_ready=True, baud=921600)
#Drone = dronekit.connect('/dev/ttyAMA0', wait_ready=True, baud=921600)

if (Drone.armed):
    Drone.armed   = False
    print("Unarmed")
else:
    Drone.armed   = True
    print("Armed")

Drone.close()