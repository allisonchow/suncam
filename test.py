import easydriver as ed
import time
import os
import datetime
print "Initializing..."

# initialize stepper
stepper_z = ed.easydriver("P8_7", 0.007, "P8_8")    # zenith
stepper_a = ed.easydriver("P8_15", 0.007, "P8_16")  # azimuthal

# rotate zenith
print "Starting zenith rotation..."
stepper_z.rotate(15)
time.sleep(1)
stepper_z.rotate(15)
time.sleep(1)
stepper_z.rotate(15)
time.sleep(1)
stepper_z.rotate(15)
time.sleep(1)
stepper_z.rotate(-60)

# rotate azimuthal
print "Starting azimuthal rotation..."
stepper_a.rotate(15)
os.system(
    "fswebcam --jpeg 100 -D 2 -F 20 -S 5 -r 1920x1080 --flip v,h '/home/suncam/fswebcampics/%s.jpg'"
    % datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
)
time.sleep(1)

print "Rotating..."
stepper_a.rotate(15)
os.system(
    "fswebcam --jpeg 100 -D 2 -F 20 -S 5 -r 1920x1080 --flip v,h '/home/suncam/fswebcampics/%s.jpg'"
    % datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
)
time.sleep(1)

print "Rotating..."
stepper_a.rotate(15)
os.system(
    "fswebcam --jpeg 100 -D 2 -F 20 -S 5 -r 1920x1080 --flip v,h '/home/suncam/fswebcampics/%s.jpg'"
    % datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
)
time.sleep(1)

print "Rotating back..."
stepper_a.rotate(-45)

print "Done"

stepper_a.finish()