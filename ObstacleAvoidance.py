'''
This script converts the distance measured by any sensor and converts it into a distance_sensor mavlink message and sends it to the FC via the telemetry port. 
For more info http://ardupilot.org/dev/docs/code-overview-object-avoidance.html The function sensor_data(d,o) encodes distance and orientation as mavlink message 
and sends them to the fc. The argument distance takes values in cm and orientation takes value as following: 
0:Front 1:Front-Right 2:Right 3:Back-Right 4:Back 5:Back-Left 6:Left 7:Front-Left 24:Up 25:Down 
For addition of more sensors, the distance can be collected and sent via the sensor_data function with the correct orientation.
'''

import dronekit
import gpiozero
import time

TRIGGER_PINS = {"Front":17,"Back":22,"Right":9,"Left":6}
ECHO_PINS = {"Front":27,"Back":10,"Right":0,"Left":13}

Orientation = {"Front":0, "Front-Right":1 ,"Right":2 ,"Back-Right":3 ,"Back":4 ,"Back-Left":5 ,"Left":6 ,"Front-Left":7, "Up":24 ,"Down":25}

FrontSensor = gpiozero.DistanceSensor(ECHO_PINS["Front"],TRIGGER_PINS["Front"])
BackSensor = gpiozero.DistanceSensor(ECHO_PINS["Back"],TRIGGER_PINS["Back"])
RightSensor = gpiozero.DistanceSensor(ECHO_PINS["Right"],TRIGGER_PINS["Right"])
LeftSensor = gpiozero.DistanceSensor(ECHO_PINS["Left"],TRIGGER_PINS["Left"])

Sensors = {"Front":FrontSensor, "Back":BackSensor, "Right":RightSensor, "Left":LeftSensor}


#Connects to the vehicle using serial port.
vehicle = dronekit.connect('/dev/serial0', wait_ready=True, baud=921600)

#Function to convert distance and orientation into a mavlink message
def SensorData(d,o):
    msg=vehicle.message_factory.distance_sensor_encode(
        0,          # Time since system boot (ignored)
        5,          # Min distance cm
        250,        # Max distance cm
        int(d),     # Current distance, must be int
        0,          # Type of sensor (ignored)
        0,          # Onboard id (ignored)
        o,          # Orientation
        0,          # Covariance (ignored)
        )
    vehicle.send_mavlink(msg)

#Simple function to measure the distance using ultrasonic sensor
def Measure():
    SensorsName = {"Front","Back","Right","Left"}

    for i in SensorsName:
        Distance = Sensors[i].distance * 100
        SensorData(Distance,Orientation[i])
        print(f"{i} = {Distance} cm")

while True:
    Measure()
