
# Calibrates the motors takes a photo for how many times you enter
# initialize zenith angle stepper


stepper = ed.easydriver("P8_7", 0.001, "P8_8")
# settings for the stepper
stepper.set_sixteenth_step()
stepper.set_direction(1)

print 'Initialized Steppers!'

# obtain 100 datapoints for the accelerometer
theta = adxl_reading.angle(True)
# rotate the stepper opposite direction from position
stepper.rotate(-theta)	##?should be stepper_z?
