import angles
from datetime import datetime
import pandas as pd
import time

import math
import easydriver as ed
import os
#Simulation initialization values
now_angle_z = 0
now_angle_a = 0
count = 0

total_moved_a = 0
total_moved_z = 0
reset = 1

# gmt = timedelta(hours = -8)
# dt = datetime(2016, 2, 26)
# end = datetime(2016, 2, 27)
# step = timedelta(minutes=5)


# result = []

# while dt < end:
    # result.append(dt)
    # dt += step


#Calculate zenith and azimuthal angles
while True:


# for i in range(1, len(result)):
    ts = pd.Timestamp(datetime.utcnow())

    zenith = angles.zenith_angle(ts, 32.879609,-117.235108)
    azimuth = angles.azimuthal_angle(ts, 32.879609,-117.235108)
    elevation = angles.elevation_angle(ts, 32.879609,-117.235108)


    #Initialize Stepper
    stepper_z = ed.easydriver("P8_7", 0.1, "P8_8")
    stepper_a = ed.easydriver("P8_15", 0.1, "P8_16")

    stepper_z.set_sixteenth_step()
    stepper_a.set_sixteenth_step()

    #numbers at the ends are the gpio pins, need a changin
    # def __init__(self,pin_step=0,delay=0.1,pin_direction=0,pin_ms1=0,pin_ms2=0,pin_ms3=0,pin_sleep=0,pin_enable=0,pin_reset=0,name="Stepper"):

    if zenith < 90: # Daytime
        # Counter
        count += 1
        # Calculate differences in current position and needed position
        if count == 1:
            now_angle_z = elevation
            now_angle_a = azimuth

        d_angle_z = elevation - now_angle_z
        d_angle_a = azimuth - now_angle_a

        ts_str = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S')

        print 'Angle Difference Z = {0}'.format(d_angle_z)
        print 'Angle Difference A = {0}'.format(d_angle_a)

        # Move stepper
        stepper_z.rotate(d_angle_z)
        stepper_a.rotate(d_angle_a) #buggy stepper

        # Update variables that keep track of current position
        now_angle_z = now_angle_z + d_angle_z
        now_angle_a = now_angle_a + d_angle_a

        total_moved_z = total_moved_z + math.fabs(d_angle_z)
        total_moved_a = total_moved_a + math.fabs(d_angle_a)

        os.system("sudo python pic.py")

        time.sleep(60)

        # Create variable that avoids reset in position
        reset = 0

        print 'Elevation = {0}'.format(now_angle_z)
        print 'Azimuth = {0}'.format(now_angle_a)
        print 'Total moved = {0}'.format(total_moved_z)

    elif zenith >= 90: # Night time

        count = 0

        if reset == 0: # reset = 0 once it comes out of day time
            # stepper_a.rotate(-total_moved_a)
            # stepper_z.rotate(-total_moved_z)
            reset = 1
            print 'I have reset!' # Sets value to something other than 0
                      # to record it has already been reset

        elif reset == 1: # If it has already been reset
            now_angle_z = 0 # Do not move
