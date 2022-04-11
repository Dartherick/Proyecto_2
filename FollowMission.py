import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil

#Arm and takeoff
def arm_and_takeoff(altitude):
    pass

def Clear_mission(vehicle):
    #---Clear the current mission
    cmds = vehicle.commands
    cmds.clear()
    vehicle.flush()

    #--download the mission again
    download_mission(vehicle)

def download_mission(vehicle):
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_read()

def get_current_mission(vehicle):
    #---download the current mission, return the number of wayspoint and the list
    print("Downloading the mission")
    download_mission(vehicle)
    missionList = []
    n_wp = 0

    for wp in vehicle.commands:
        missionList.append(wp)
        n_wp += 1

    return n_wp, missionList

def add_last_waypoint(vehicle, lat, long, alt):
    #-- Adds a last waypoint to a mission list
    download_mission()
    #cmds = vehicle.commands
    cmds = download_mission(vehicle)

    #-- Save the mission to a temporary List
    missionList = []
    for wp in cmds:
        missionList.append(wp)

    #-- Append a last waypoint
    wp_last = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                      0, 0, 0, 0, 0, 0,
                      lat, long, alt)
    
    missionList.append(wp_last)

    #-- We clear the current mission
    cmds.clear()

    #-- We write the new mission
    for wp in missionList:
        cmds.add(wp)

    cmds.upload()

    return (cmds.count)

def ChangeMode(vehicle, mode):
    #-- Change autopilot mode
    while vehicle.mode != vehicle(mode):
        vehicle.mode = vehicleMode(mode)
        time.sleep(0.5)

    return True

#---------Initilize
gnd_speed = 10
mode = 'Ground'

#---------Connect
vehicle = dronekit.connect('/dev/serial0', wait_ready=True, baud=921600)

#Main function
while True:
    if mode == 'GROUND':
        #Wait until a valid mission has been uploaded 
        n_wp, missionList = get_current_mission(vehicle)
        time.sleep(2)

        if n_wp > 0:
            print('A valid mission has been uploaded: takeoff')
            mode = 'TAKEOFF'

    elif mode == 'TAKEOFF':
        #Add the current position as last waypoint
        add_last_waypoint_to_mission(vehicle,
                                     vehicle.location.gloval_relative_frame.lat,
                                     vehicle.location.global_relative_frame.lon,
                                     vehicle.location.global_relative_frame.alt)
        
        print('Final waypoint added to the current mission')
        time.sleep(1)

        #Takeoff
        arm_and_takeoff(10)

        #Change mode to AUTO
        ChangeMode(vehicle,'AUTO')

        #Set the ground speed
        vehicle.groundspeed = gnd_speed

        mode = 'MISSION'
        print('Switch to MISSION mode')

    elif mode == 'MISSION':
        #we monitor the mission, when the current waypoint is equal to the number of wp
        #We go back home, we claer the mission and land

        print(f'Currrent WP: {vehicle.commands.next} of {vehicle.commands.count}')

        if (vehicle.commands.next == vehicle.commands.count):
            print('Final wp reached: go back home')

            #clear the mission
            Clear_mission(vehicle)
            print('Mission deleted')

            ChangeMode(vehicle,'RTL')
            
            mode = 'BACK'

    elif mode == 'BACK':
        #When altitude is below 1, switch to GROUND mode
        if vehicle.location.global_relative_frame.alt < 1.0:
            print('Vehicle landed, back to GROUND')
            mode = 'GROUND'

    time.sleep(0.5)