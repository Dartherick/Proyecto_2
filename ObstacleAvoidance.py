import dronekit
import RPi.GPIO as GPIO
import time

#{TRIG,ECHO}
FrontSensor = {4,17}
BackSensor = {27,22}
RightSensor = {10,9}
LeftSensor = {11,5}

#
Orientation = {0:"Forward", 1:"Forward-Right", 2:"Right", 3:"Back-Right", 4:"Back", 5:"Back-Left", 6:"Left", 7:"Forward-Left" ,24:"Up", 25:"Down"}

GPIO.setmode(GPIO.BCM)

GPIO.setup(FrontSensor[0],GPIO.OUT)
GPIO.setup(FrontSensor[1],GPIO.IN)

GPIO.setup(BackSensor[0],GPIO.OUT)
GPIO.setup(BackSensor[1],GPIO.IN)

GPIO.setup(LeftSensor[0],GPIO.OUT)
GPIO.setup(LeftSensor[1],GPIO.IN)

GPIO.setup(RightSensor[0],GPIO.OUT)
GPIO.setup(RightSensor[1],GPIO.IN)

#Connects to the vehicle using serial port.
vehicle = dronekit.connect('/dev/ttyS0', wait_ready=True, baud=57600)

#Function to convert distance and orientation into a mavlink message
def sensor_data(d,o):
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
def measure(Sensor):
    dist1 = 250
    GPIO.output(Sensor[0], True)
    time.sleep(0.00001)
    GPIO.output(Sensor[0], False)
    echo_state = 0
	
    while echo_state == 0:
        echo_state = GPIO.input(Sensor[0])
        pulse_start = time.time()
			
    while GPIO.input(Sensor[0])==1:
        pulse_end = time.time()
			
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
	
    if(distance < 250 and distance > 5): #To filter out junk values
        dist1 = distance
			
    sensor_data(dist1,0) #Sends measured distance(dist1) and orientation(0) as a mavlink message.
    return dist1

# Main code
if __Name__ == __Main__:
	while True:
	    d = measure()
	    time.sleep(0.1)
	    print(d)