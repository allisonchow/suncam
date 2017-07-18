import angles
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
import math
import easydriver as ed
import os
import adxl_reading

# Simulation initialization values
now_angle_z = 0.0
now_angle_a = 0.0
count = 0.0     ##increments during day, 0 at night

total_moved_a = 0.0
total_moved_z = 0.0
reset = 1.0     ##indicates whether it has been reset; sets to anything other than 0 to indicate it's been reset

os.system("sudo python adxl_cal.py")    ##adafruit_bbio (beaglebone library) can only be run with sudo
time.sleep(2)   ##pauses code for 2 sec; whats the purpose?
os.system("sudo python adxl_cal.py")    

gmt = timedelta(hours=5)    ##?isnt it a 7hr diff from SD time to GMT? 
dt = datetime(2016, 6, 20)  ##?should make this a user input?
end = datetime(2016, 6, 21) ##?should make this a user input?
step = timedelta(minutes=5) ##reformats into a change in time

# Initialize Stepper
stepper_z = ed.easydriver("P8_7", 0.1, "P8_8")
stepper_a = ed.easydriver("P8_15", 0.1, "P8_16")

stepper_z.set_sixteenth_step()  ##sets outputs of microsteps as true
stepper_a.set_sixteenth_step()

result = []

while dt < end: ##while the current time is less than the end time, add the time to the array and increment the current time
    result.append(dt)   ##add the dt to the result array
    dt += step ##adds variable step (the change in time) to dt (current time) and reassigns the value to dt

##create the dataframe for the output values
df = pd.DataFrame(
    columns=['timestamp', 'd_angle', 'elevation', 'measured']
)   ##a data frame is like a cluster but with labled axes

df.to_csv('indoors_data.csv')   ##sends the datafram to a comma-separated values file, named indoors_data
##indoors_data is a dataframe of each time and its corresponding position

# Calculate zenith and azimuthal angles
for i in range(1, len(result)): ##from 1 to the length of result array (list of times); iterates at each time
        ##?so does the length get recalculated every time the time updates?
    ts = pd.Timestamp(result[i])    ##assigns ts as the timestamp version of the time at i
    zenith = angles.zenith_angle(ts + gmt, 32.879609, -117.235108)  ##calculates zenith at given time in GMT and coordinates of SERF building
    azimuth = angles.azimuthal_angle(ts + gmt, 32.879609, -117.235108)  
    elevation = angles.elevation_angle(ts + gmt, 32.879609, -117.235108)

    if zenith < 90.0:   ##if daytime
        # Daytime

        # Calculate differences in current position and needed position
        if count == 0:  ##
            now_angle_z = 0.0   ##?why are we reinitializing these again? already did this at the beginning
            now_angle_a = azimuth  # remember to change this back to 0
            # should change to adxl calibration ##for zenith

        d_angle_z = elevation - now_angle_z ##difference between haurwitz calcs and current angle
        d_angle_a = azimuth - now_angle_a   ##difference between haurwitz calcs and current angle

        # ts_str = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S')

        print '-------------Time: {0}---------------'.format(ts)
        print 'Angle Difference Z = {0}'.format(d_angle_z)
        print 'Angle Difference A = {0}'.format(d_angle_a)

        # Move stepper
        stepper_z.rotate(d_angle_z) ##rotates zenith the calculated angle difference
        # stepper_z.rotate(d_angle_z)

        stepper_a.rotate(d_angle_a) ##rotates azimuth the calculated angle difference

        # Update variables that keep track of current position
        now_angle_z = now_angle_z + d_angle_z
        now_angle_a = now_angle_a + d_angle_a

        total_moved_z = total_moved_z + math.fabs(d_angle_z)    ##total moved is initialized as 0 in beginning
        total_moved_a = total_moved_a + math.fabs(d_angle_a)    ##math.fabs returns absolute value

        # Create variable that avoids reset in position

        reset = 0   ##?why is it necessary to reset it to 0 on every iteration? isn't it already at 0?

        print 'Elevation = {0}'.format(now_angle_z) 
        print 'Azimuth = {0}'.format(now_angle_a)
        theta = adxl_reading.angle(True)    ##uses accelerometer to find the angle position
        print 'Calculated Angle = {0}'.format(theta)    ##?shouldnt this be the measured angle??
        # end of day time

        # Counter
        count += 1  ##increments the counter

        # save the information into a pandas dataframe

        df = pd.read_csv('indoors_data.csv', index_col=0)   ##creates an index column in the dataframe

        df.loc[len(df)] = [ts, d_angle_z, elevation, theta] ##inputs values into the last position of the dataframe with each iteration

        df.to_csv('indoors_data.csv')   ##saves the new dataframe each time

        time.sleep(5)   ##pauses code for 5 sec; whats the purpose?

    elif zenith >= 90.0:    ##then nighttime
        # Night time
        count = 0

        if reset == 0:  ##if it hasnt been reset yet
            # reset = 0 once it comes out of day time

            stepper_a.rotate(-total_moved_a)    ##then rotate the motor the total moved in the opposite direction to achieve original position
            os.system("sudo python adxl_cal.py")    ##uses accelerometer to determine zenith position; resets to original position
            reset = 1   ##indicates that it has been reset

            print 'I have reset!'
            # Sets value to something other than 0
            # To record it has already been reset

        elif reset == 1:
            # If it has already been reset
            now_angle_z = 0     ##?why is this necessary?
            # Do not move
