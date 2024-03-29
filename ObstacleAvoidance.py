'''
This script converts the distance measured by any sensor and converts it into a distance_sensor mavlink message and sends it to the FC via the telemetry port. 
For more info http://ardupilot.org/dev/docs/code-overview-object-avoidance.html The function sensor_data(d,o) encodes distance and orientation as mavlink message 
and sends them to the fc. The argument distance takes values in cm and orientation takes value as following: 
0:Front 1:Front-Right 2:Right 3:Back-Right 4:Back 5:Back-Left 6:Left 7:Front-Left 24:Up 25:Down 
For addition of more sensors, the distance can be collected and sent via the sensor_data function with the correct orientation.
'''

import gpiozero

Orientation = {"Front":0, "Front-Right":1 ,"Right":2 ,"Back-Right":3 ,"Back":4 ,"Back-Left":5 ,"Left":6 ,"Front-Left":7, "Up":24 ,"Down":25}

class UltrasonicSensors():
    def __init__(self,ECHO_PINS,TRIGGER_PINS):
        FrontSensor = gpiozero.DistanceSensor(ECHO_PINS["Front"],TRIGGER_PINS["Front"])
        #BackSensor = gpiozero.DistanceSensor(ECHO_PINS["Back"],TRIGGER_PINS["Back"])
        RightSensor = gpiozero.DistanceSensor(ECHO_PINS["Right"],TRIGGER_PINS["Right"])
        LeftSensor = gpiozero.DistanceSensor(ECHO_PINS["Left"],TRIGGER_PINS["Left"])

        #self.SensorsList = {"0":FrontSensor,"2":RightSensor,"6":LeftSensor,"4":BackSensor}
        self.SensorsList = {"0":FrontSensor,"2":RightSensor,"6":LeftSensor}

    #Simple function to measure the distance using ultrasonic sensor
    def Measure(self,Sensors,Gain,t):
        for i in Sensors:
            Distance = self.SensorsList[i].distance * 100 * Gain
            #SensorData(Distance,Orientation[i])
            print(f"{i} = {Distance} cm - {Distance/100} m")

#Measure(5,0.05)


