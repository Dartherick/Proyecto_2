import dronekit
import time

#Connects to the vehicle using serial port.
vehicle = dronekit.connect('/dev/ttyS0', wait_ready=True, baud=921600)
#vehicle = dronekit.connect('/dev/ttyS0', wait_ready=True, baud=5760)

if (vehicle.armed):
    vehicle.armed   = False
    print("Unarmed")
else:
    vehicle.armed   = True
    print("Armed")

vehicle.close()