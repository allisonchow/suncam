import angles_update
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
import math
import easydriver as ed
import os
##import adafruit_adxl345 as adxl345


print "Setting variables..."


gmt = timedelta(hours=5) 
dt = datetime(2017, 7, 10)
end = datetime(2017, 7, 11)    ##update this
step = timedelta(minutes=5) ##reformats into a change in time
result = [] ##list of times
now_angle_z = 0.0
now_angle_a = 0.0
count = 0.0     ##increments during day, 0 at night
total_moved_a = 0.0
total_moved_z = 0.0
reset = 1.0     ##indicates whether it has been reset; sets to anything other than 0 to indicate it's been reset


print "Initializing..."  


# Initialize Stepper
stepper_z = ed.easydriver("P8_7", 0.007, "P8_8")    ##changed to 0.007 for test
stepper_a = ed.easydriver("P8_15", 0.007, "P8_16")

##stepper_z.set_sixteenth_step()  ##sets resolution to 1/16th
##stepper_a.set_sixteenth_step()  ##must be string; fix this


print "Setting Time Table"


while dt < end: ##while the current time is less than the end time, add the time to the array and increment the current time
    result.append(dt)   ##add the dt to the result array
    dt += step ##adds variable step (the change in time) to dt (current time) and reassigns the value to dt

df = pd.DataFrame(columns = ['timestamp', 'change in zenith/elevation angle', 'Haurwitz elevation', 'counter'])
    ##columns = ['timestamp', 'change in zenith/elevation angle', 'Haurwitz elevation', 'measured elevation angle', 'counter']
    ##added column for counter, updated names of column
df.to_csv('indoors_data.csv')   ##sends the datafram to a comma-separated values file, named indoors_data
##indoors_data is a dataframe of each time and its corresponding position



print "Beginning calculations"


# Calculate zenith and azimuthal angles
for i in range(1, len(result)): 

    ##first gets current time and position
    ts = pd.Timestamp(result[i])    ##assigns ts as the timestamp version of the time at i
    zenith = angles_update.zenith_angle(gmt + ts, 32.879609, -117.235108)  ##calculates zenith at given time in GMT and coordinates of SERF building
    azimuth = angles_update.azimuthal_angle(gmt + ts, 32.879609, -117.235108)  
    elevation = angles_update.elevation_angle(gmt + ts, 32.879609, -117.235108) 

    if zenith < 90.0:
        # Daytime

        # Calculate differences in current position and needed position
        if count == 0:  ##
            ##now_angle_z = theta   ##changed to adxl calibration
            now_angle_z = 0.0
            now_angle_a = 0.0

        d_angle_z = elevation - now_angle_z ##difference between haurwitz calcs and current angle
        d_angle_a = azimuth - now_angle_a   ##difference between haurwitz calcs and current angle

        # ts_str = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S')

        print '-------------Time: {0}---------------'.format(ts)
        print 'Angle Difference Z = {0}'.format(d_angle_z)
        print 'Angle Difference A = {0}'.format(d_angle_a)

        # Move stepper
        stepper_z.rotate(d_angle_z) ##rotates zenith the calculated angle difference
        stepper_a.rotate(d_angle_a) ##rotates azimuth the calculated angle difference

        # Update variables that keep track of current position
        now_angle_z = now_angle_z + d_angle_z
        now_angle_a = now_angle_a + d_angle_a

        total_moved_z = total_moved_z + math.fabs(d_angle_z)    ##total moved is initialized as 0 in beginning
        total_moved_a = total_moved_a + math.fabs(d_angle_a)    ##math.fabs returns absolute value

        # Create variable that avoids reset in position

        reset = 0   ##?why is it necessary to reset it to 0 on every iteration? isn't it already at 0?

        print 'Updated Elevation = {0}'.format(now_angle_z) 
        print 'Updated Azimuth = {0}'.format(now_angle_a)
        ##theta = adxl_reading.angle(True)    ##uses accelerometer to find the angle position
        ##print 'Measured Angle = {0}'.format(theta)    ##?shouldnt this be the measured angle??
        # end of day time

        # Counter

        count += 1  ##increments the counter

        # save the information into a pandas dataframe

        df = pd.read_csv('indoors_data.csv', index_col=0)   ##creates an index column in the dataframe

        ##df.loc[len(df)] = [ts, d_angle_z, elevation, theta, count] ##inputs values into the last position of the dataframe with each iteration
        df.loc[len(df)] = [ts, d_angle_z, elevation, count] ##inputs values into the last position of the dataframe with each iteration

        df.to_csv('indoors_data.csv')   ##saves the new dataframe each time

        time.sleep(30)   ##pauses code for 30s; later change to 5 min

    elif zenith >= 90.0:
        # Night time
        count = 0

        if reset == 0:  ##if it hasnt been reset yet
            # reset = 0 once it comes out of day time

            stepper_a.rotate(-total_moved_a)    ##then rotate the motor the total moved in the opposite direction to achieve original position
            ##os.system("sudo python adxl_cal.py")    ##uses accelerometer to determine zenith position; resets to original position
            stepper_z.rotate(-total_moved_z)    ##later just use above line
            reset = 1   ##indicates that it has been reset

            print 'I have reset!'
            # Sets value to something other than 0
            # To record it has already been reset

        elif reset == 1:
            # If it has already been reset
            now_angle_z=0 ##why is this neccessary
            # Do not move

##need to add camera

"""
suncam@coimbra-beagle11:~$ sudo python newmotors_update.py
Setting variables...
Initializing...
Setting Time Table
Beginning calculations
Traceback (most recent call last):
  File "newmotors_update.py", line 63, in <module>
    zenith = angles_update.zenith_angle(ts + gmt, 32.879609, -117.235108)  ##calculates zenith at given time in GMT and coordinates of SERF building
  File "/home/suncam/angles_update.py", line 136, in zenith_angle
    return solar_angles(df, lat, lon, alt=alt)[:, 0]
  File "/home/suncam/angles_update.py", line 61, in solar_angles
    idf = df.index  ##need index array of df
AttributeError: 'Timestamp' object has no attribute 'index'
"""