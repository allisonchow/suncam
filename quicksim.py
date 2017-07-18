import angles
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
import math
import easydriver as ed
import os
##?should also import adxl?

# Simulation initialization values
now_angle_z = 0.0
now_angle_a = 0.0
count = 0.0

total_moved_a = 0.0
total_moved_z = 0.0
reset = 1.0

#os.system("sudo python adxl_cal.py")
#time.sleep(2)
#os.system("sudo python adxl_cal.py")

gmt = timedelta(hours=5)
dt = datetime(2016, 6, 20)
end = datetime(2016, 6, 21)
step = timedelta(minutes=5)

# Initialize Stepper
stepper_z = ed.easydriver("P8_7", 0.007, "P8_8")
stepper_a = ed.easydriver("P8_15", 0.007, "P8_16")

# set step resolution
#stepper_z.set_sixteenth_step()
#stepper_a.set_sixteenth_step()

result = []

while dt < end:
    result.append(dt)
    dt += step



# Calculate zenith and azimuthal angles
for i in range(1, len(result)):

    ts = pd.Timestamp(result[i])
    zenith = angles.zenith_angle(ts + gmt, 32.879609, -117.235108)
    azimuth = angles.azimuthal_angle(ts + gmt, 32.879609, -117.235108)
    elevation = angles.elevation_angle(ts + gmt, 32.879609, -117.235108)

    if zenith < 90.0:
        # Daytime

        # Calculate differences in current position and needed position
        if count == 0:
            now_angle_z = 0.0
            now_angle_a = azimuth  # remember to change this back to 0
            # should change to adxl calibration

        d_angle_z = elevation - now_angle_z
        d_angle_a = azimuth - now_angle_a

        # ts_str = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S')


        # Move stepper
        stepper_z.rotate(d_angle_z)
        # stepper_z.rotate(d_angle_z)

        stepper_a.rotate(d_angle_a)

        # Update variables that keep track of current position
        now_angle_z = now_angle_z + d_angle_z
        now_angle_a = now_angle_a + d_angle_a

        total_moved_z = total_moved_z + math.fabs(d_angle_z)
        total_moved_a = total_moved_a + math.fabs(d_angle_a)

        # Create variable that avoids reset in position

        reset = 0
        # end of day time

        # Counter
        count += 1

        # save the information into a pandas dataframe

        time.sleep(.1)

    elif zenith >= 90.0:
        # Night time
        count = 0

        if reset == 0:
            # reset = 0 once it comes out of day time

            stepper_a.rotate(-total_moved_a)
            reset = 1

            print 'I have reset!'
            # Sets value to something other than 0
            # To record it has already been reset

        elif reset == 1:
            # If it has already been reset
            now_angle_z = 0
            # Do not move
