""" 
Solar tracking device with camera, BBB, and 2 motors. No sensors are used in this code (accelerometer, etc.).
Image processing used as feedback system.
Multiple test checkpoints highlighted throughout code (may be removed after testing).
4 user inputs regarding time and location highlighted throughout code.
"""

import angles
import imageprocessing
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
import math
import easydriver as ed
import os
from imageprocessing import sun_center
from imageprocessing import rotate_center


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
stepper_a = ed.easydriver("P8_7", 0.007, "P8_8", "P8_26", "P8_9", "P8_10")
stepper_z = ed.easydriver("P8_17", 0.007, "P8_18", "P8_14", "P8_15", "P8_16")

stepper_z.set_sixteenth_step()
stepper_a.set_sixteenth_step()


# Initialize times
while dt <= end:
    result.append(dt)
    dt += step


# Initialize dataframe
df = pd.DataFrame(columns = ['Timestamp', 'Calculated Elevation', 'Change in Elevation', 'Calculated Azimuthal', 'Change in Azimuthal', 'Horizontal Offset', 'Vertical Offset'])

df.to_csv('{0}_testdata.csv'.format(dt.strftime("%Y%m%d")))


# Iterate at each time
for i in range(0, (len(result))):

    print 'Iteration: {0}'.format(i)    ## remove after testing

    # Calculate current time and position
    ts = pd.Timestamp(result[i])
    zenith = angles.zenith_angle(gmt + ts, 32.879609, -117.235108)  #-----4. location coordinates (SERF building)-----#
    azimuth = angles.azimuthal_angle(gmt + ts, 32.879609, -117.235108)  
    elevation = angles.elevation_angle(gmt + ts, 32.879609, -117.235108)
    img = ts.strftime("%Y%m%d_%H%M%S") 


    # If more than half a step behind schedule, skip this iteration
    if (datetime.utcnow() - gmt) > (ts + (step/2)): 

        print 'Could not capture image at {0}'.format(img)

        # Null dataframe variables
        d_angle_z = 'NA'
        d_angle_a = 'NA' 

        # Counter
        count += 1

        # Create variable that avoids reset in position
        reset = 0


    # If on schedule
    else:


        # Daytime
        if zenith < 90.0:
    

            # Initializes angles
            if count==0:
                now_angle_z = 0    # actually elevation ## update after testing
                now_angle_a = 0   ## update after testing

            # Calculate differences in current position and needed position
            d_angle_z = elevation - now_angle_z # now_angle_z is actually elevation 
            d_angle_a = azimuth - now_angle_a

            print '-------------Time: {0}---------------'.format(ts)
            print '---------Actual Time: {0}---------'.format(datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S'))  ## remove after testing
            print 'Angle Difference Z = {0}'.format(d_angle_z)
            print 'Angle Difference A = {0}'.format(d_angle_a)

            # Move stepper
            d_angle_z = stepper_z.rotate(d_angle_z) 
            d_angle_a = stepper_a.rotate(d_angle_a)

            # Update variables that keep track of current position
            now_angle_z = now_angle_z + d_angle_z
            now_angle_a = now_angle_a + d_angle_a

            total_moved_z = total_moved_z + d_angle_z
            total_moved_a = total_moved_a + d_angle_a

            print 'Updated Elevation = {0}'.format(now_angle_z) 
            print 'Updated Azimuth = {0}'.format(now_angle_a)

            # Take picture
            os.system(
                "fswebcam --jpeg 100 -D 2 -F 20 -S 5 -r 1920x1080 --flip v,h '/home/suncam/fswebcampics/{0}.jpg'".format(img)
            )


            # If picture is taken, complete image processing feedback loop
            if os.path.isfile('/home/suncam/fswebcampics/{0}.jpg'.format(img)) == True:

                # Find sun center using image processing
                [dist_x, dist_y] = sun_center(img)

                # Feedback loop
                thresh = 20 ## Determine proper threshold
                k = 1   # Counter

                while dist_x > thresh or dist_y > thresh:

                    # Rotate motor
                    [degree_a, degree_z] = rotate_center(dist_x, dist_y)

                    # Take picture
                    os.system(
                        "fswebcam --jpeg 100 -D 2 -F 20 -S 5 -r 1920x1080 --flip v,h '/home/suncam/fswebcampics/{0} LOOP {1}.jpg'".format(img, k)
                    )

                    # Find new sun center
                    [dist_x, dist_y] = sun_center("{0} LOOP {1}".format(img, k))

                    # Counter
                    k += 1


            # Counter
            count += 1

            # Create variable that avoids reset in position
            reset = 0

        
        # Night
        else:

            # Null dataframe variables
            d_angle_z = 'NA'
            d_angle_a = 'NA'

            # Counter
            count = 0


            # Needs to be reset
            if reset == 0:
                
                print 'It is night!'

                d_angle_a = stepper_a.rotate(-total_moved_a)
                d_angle_z = stepper_z.rotate(-total_moved_z)

                total_moved_a = total_moved_a + d_angle_a
                total_moved_z = total_moved_z + d_angle_z

                reset = 1   

                print 'I have reset!'


    # Save information into dataframe
    df = pd.read_csv('{0}_testdata.csv'.format(dt.strftime("%Y%m%d")), index_col = 0)
    
    df.loc[len(df)] = [ts, elevation, d_angle_z, azimuth, d_angle_a, dist_x, dist_y] 
    
    df.to_csv('{0}_testdata.csv'.format(dt.strftime("%Y%m%d")))


    # Determines how long to sleep
    if i < (len(result)-1): 

        tsleep = (pd.Timestamp(result[i + 1]) - (datetime.utcnow() - gmt)).total_seconds()

        if tsleep > 0:

            time.sleep(tsleep)


    # If last iteration, then end
    else:

        d_angle_a = stepper_a.rotate(-total_moved_a)
        d_angle_z = stepper_z.rotate(-total_moved_z)

        total_moved_a = total_moved_a + d_angle_a
        total_moved_z = total_moved_z + d_angle_z
        
        reset = 1 
        
        # Display dataframe
        pd.set_option('display.max_rows', len(df))  ## remove after testing
        print(df)

        print '--------------Ending solar tracking at {0}--------------'.format(datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S'))