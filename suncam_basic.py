""" 
Solar tracking device with camera, BBB, and 2 motors. No sensors are used in this code (accelerometer, etc.).
Multiple test checkpoints highlighted throughout code (may be removed after testing).
4 user inputs regarding time and location highlighted throughout code.
"""

import angles
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
import math
import easydriver as ed
import os


# Simulation initialization values
now_angle_z = 0.0
now_angle_a = 0.0
count = 0.0

total_moved_a = 0.0
total_moved_z = 0.0
reset = 1.0     # if reset, =1; if not reset, =0


# Update settings
gmt = timedelta(hours = 7) #-----1. time difference between location and GMT/UTC (depends on daylight savings)-----#
dt = datetime.utcnow() - gmt
# dt = datetime(2017, 7, 10)
end = dt + timedelta(hours = 3)  #-----2. duration of tracking-----#
# end = datetime(2017, 7, 11)
step = timedelta(minutes = 5)  #-----3. tracking intervals-----#
result = []


# Initialize Stepper
stepper_z = ed.easydriver("P8_7", 0.007, "P8_8")    ## changed to 0.007 for test
stepper_a = ed.easydriver("P8_15", 0.007, "P8_16")

## stepper_z.set_sixteenth_step()  # sets resolution to 1/16th
## stepper_a.set_sixteenth_step()  ## must be string; fix this


# Initialize times
while dt <= end:
    result.append(dt)
    dt += step


# Initialize dataframe
df = pd.DataFrame(columns = ['Timestamp', 'Calculated Elevation', 'Change in Elevation', 'Calculated Azimuthal', 'Change in Azimuthal'])

df.to_csv('indoors_data.csv')


# Iterate at each time
for i in range(1, (len(result)+1)):


    print 'Iteration: {0}'.format(i)    ## remove after testing
    

    # Calculate current time and position
    ts = pd.Timestamp(result[i-1])
    zenith = angles.zenith_angle(gmt + ts, 32.879609, -117.235108)  #-----4. location coordinates (SERF building)-----#
    azimuth = angles.azimuthal_angle(gmt + ts, 32.879609, -117.235108)  
    elevation = angles.elevation_angle(gmt + ts, 32.879609, -117.235108) 


    # If more than half a step behind schedule, skip this iteration
    if (datetime.utcnow() - gmt) > (ts + (step/2)): 
 

        print 'Could not capture image at {0}'.format(ts)


        # Null dataframe variables
        d_angle_z = 'NA'
        d_angle_a = 'NA' 


        # Counter
        count += 1


        # Create variable that avoids reset in position
        reset = 0

    

    # If on schedule
    elif (datetime.utcnow() - gmt) <= (ts + (step/2)):


        # Daytime
        if zenith < 90.0:
        

            # Initializes angles
            if count==0:
                now_angle_z = 0    ## update after testing
                now_angle_a = 0   ## update after testing



            # Calculate differences in current position and needed position
            d_angle_z = elevation - now_angle_z
            d_angle_a = azimuth - now_angle_a

            print '-------------Time: {0}---------------'.format(ts)
            print '---------Actual Time: {0}---------'.format(datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S'))  ## remove after testing
            print 'Angle Difference Z = {0}'.format(d_angle_z)
            print 'Angle Difference A = {0}'.format(d_angle_a)


            # Move stepper
            stepper_z.rotate(-d_angle_z)
            stepper_a.rotate(-d_angle_a)


            # Update variables that keep track of current position
            now_angle_z = now_angle_z + d_angle_z
            now_angle_a = now_angle_a + d_angle_a

            total_moved_z = total_moved_z + math.fabs(d_angle_z)
            total_moved_a = total_moved_a + math.fabs(d_angle_a)

            print 'Updated Elevation = {0}'.format(now_angle_z) 
            print 'Updated Azimuth = {0}'.format(now_angle_a)


            # Take picture
            os.system(
                "fswebcam --jpeg 100 -D 2 -F 20 -S 5 -r 1920x1080 --flip v,h '/home/suncam/fswebcampics/%s.jpg'"
                % ts.strftime("%Y%m%d_%H%M%S")
            )


            # Counter
            count += 1


            # Create variable that avoids reset in position
            reset = 0

        
        # Night
        elif zenith >= 90.0:
            

            # Null dataframe variables
            d_angle_z = 'NA'
            d_angle_a = 'NA'


            # Counter
            count = 0


            # Needs to be reset
            if reset == 0:
                
                print 'It is night!'

                stepper_a.rotate(-total_moved_a)
                stepper_z.rotate(-total_moved_z)
                
                reset = 1   

                print 'I have reset!'


    # Save information into dataframe
    df = pd.read_csv('indoors_data.csv', index_col = 0)
    
    df.loc[len(df)] = [ts, elevation, d_angle_z, azimuth, d_angle_a] 
    
    df.to_csv('indoors_data.csv')


    # Determines how long to sleep
    if i < len(result): 

        tsleep = (pd.Timestamp(result[i]) - (datetime.utcnow() - gmt)).total_seconds()

        if tsleep >= 0:

            time.sleep(tsleep)


    # If last iteration, then end
    elif i >= len(result):

        tsleep = 0
        
        # Display dataframe
        pd.set_option('display.max_rows', len(df))  ## remove after testing
        print(df)

        print '--------------Ending solar tracking at {0}--------------'.format(datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S'))