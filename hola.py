import ObstacleAvoidance as ad

hola = ad.Sensor(4)
print(hola.klk)

#Function to convert distance and orientation into a mavlink message
def SensorData(d,o):
    msg=vehicle.message_factory.distance_sensor_encode(
        0,          # Time since system boot (ignored)
        5,          # Min distance cm
        500,        # Max distance cm
        int(d),     # Current distance, must be int
        1,          # Type of sensor (ignored)
        0,          # Onboard id (ignored)
        o,          # Orientation
        0,          # Covariance (ignored)
        )
    vehicle.send_mavlink(msg)

