import threading
import dronekit
import time
import ObstacleAvoidance as OA
from Proyecto_2.ObstacleAvoidance import Sensors, UltrasonicSensors

#Connects to the vehicle using serial port.
#timeout = kwargs.get('timeout', 30)
Drone = dronekit.connect('/dev/serial0', wait_ready=True, baud=921600)

TRIGGER_PINS = {"Front":6,"Back":17,"Right":9,"Left":22}
ECHO_PINS = {"Front":13,"Back":27,"Right":0,"Left":10}

SensorOrientation = (0,2,6)

#Function to convert distance and orientation into a mavlink message
def SensorData(d,o):
    msg=Drone.message_factory.distance_sensor_encode(
        0,          # Time since system boot (ignored)
        5,          # Min distance cm
        500,        # Max distance cm
        int(d),     # Current distance, must be int
        1,          # Type of sensor (ignored)
        0,          # Onboard id (ignored)
        o,          # Orientation
        0,          # Covariance (ignored)
        )
    Drone.send_mavlink(msg)

Sensors = OA.UltrasonicSensors(
	
	ECHO_PINS,TRIGGER_PINS)
Sensors.Measure(SensorOrientation,5)


'''# Don't let the user try to arm until autopilot is ready
while not Drone.is_armable:
	print (" Waiting for vehicle to initialise...")
	time.sleep(1)

if (Drone.armed):
	Drone.armed  = False
	print("Unarmed")
else:
	Drone.armed   = True
	Drone.mode = dronekit.VehicleMode("GUIDED")
	print("Armed")
'''
Drone.close()
