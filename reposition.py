"""
Use to reposition camera
"""


import easydriver as ed


# Initialize Stepper
stepper_a = ed.easydriver("P8_9", 0.007, "P8_10", "P8_7", "P8_8", "P8_26")
stepper_z = ed.easydriver("P8_17", 0.007, "P8_18", "P8_14", "P8_15", "P8_16")



# Move stepper
stepper_a.rotate(10)   ## CW
stepper_a.rotate(-10)	## CCW


stepper_z.rotate(10)	## Up
stepper_z.rotate(-10)	## Down
