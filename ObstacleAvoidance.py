'''
This script converts the distance measured by any sensor and converts it into a distance_sensor mavlink message and sends it to the FC via the telemetry port. 
For more info http://ardupilot.org/dev/docs/code-overview-object-avoidance.html The function sensor_data(d,o) encodes distance and orientation as mavlink message 
and sends them to the fc. The argument distance takes values in cm and orientation takes value as following: 
0:Forward 1:Forward-Right 2:Right 3:Back-Right 4:Back 5:Back-Left 6:Left 7:Forward-Left 24:Up 25:Down 
For addition of more sensors, the distance can be collected and sent via the sensor_data function with the correct orientation.
'''

import dronekit
import gpiozero
import time

ECHO_PINS = {"Front":17,"Back":22,"Right":9,"Left":5}
TRIGGER_PINS = {"Front":4,"Back":27,"Right":10,"Left":11}

Orientation = {0:"Forward", 1:"Forward-Right", 2:"Right", 3:"Back-Right", 4:"Back", 5:"Back-Left", 6:"Left", 7:"Forward-Left" ,24:"Up", 25:"Down"}

FrontSensor = gpiozero.DistanceSensor(ECHO_PINS["Front"],TRIGGER_PINS["Front"])
BackSensor = gpiozero.DistanceSensor(ECHO_PINS["Back"],TRIGGER_PINS["Back"])
RightSensor = gpiozero.DistanceSensor(ECHO_PINS["Right"],TRIGGER_PINS["Right"])
LeftSensor = gpiozero.DistanceSensor(ECHO_PINS["Left"],TRIGGER_PINS["Left"])


#Connects to the vehicle using serial port.
vehicle = dronekit.connect('/dev/ttyS0', wait_ready=True, baud=57600)

#Function to convert distance and orientation into a mavlink message
def SensorData(d,o):
    msg=vehicle.message_factory.distance_sensor_encode(
        0,
        5,
        250,
        d,
        0,
        1,
        o,
        0,
        )
    vehicle.send_mavlink(msg)

#Simple function to measure the distance using ultrasonic sensor
def Measure():
    Sensors = {"Front","Back","Right","Left"}

    for i in Sensors:
        d = gpiozero.DistanceSensor(ECHO_PINS[i],TRIGGER_PINS[i]).distance()
        SensorData(d,)


# Main code
#if __Name__ == __main__: