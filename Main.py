import dronekit
import time

#Connects to the vehicle using serial port (/dev/ttyAMA0).
Drone = dronekit.connect('/dev/ttyS0', wait_ready=True, timeout=300, baud=921600)

# Don't let the user try to arm until autopilot is ready

while not Drone.is_armable:
	print " Waiting for vehicle to initialise..."
	time.sleep(1)

if (Drone.armed):
	Drone.armed   = False
	print("Unarmed")
else:
	Drone.armed   = True
	Drone.mode = dronekit.VehicleMode("GUIDED")
	print("Armed")

Drone.close()