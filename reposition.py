"""
Use to reposition camera.
Use RHR 
"""


import easydriver as ed
import os


# Initialize Stepper
stepper_z = ed.easydriver("P8_7", 0.007, "P8_8")
stepper_a = ed.easydriver("P8_15", 0.007, "P8_16")

stepper_z.set_sixteenth_step  # sets resolution to 1/16th
stepper_a.set_sixteenth_step  ## must be string; fix this



# Move stepper
stepper_z.rotate(-95)	## input zenith rotation
stepper_a.rotate(180)	## input azimuth rotation