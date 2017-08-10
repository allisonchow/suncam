"""
Use to reposition camera
"""


import easydriver as ed


# Initialize Stepper
stepper_a = ed.easydriver("P8_7", 0.007, "P8_8", "P8_26", "P8_9", "P8_10")
stepper_z = ed.easydriver("P8_17", 0.007, "P8_18", "P8_14", "P8_15", "P8_16")

stepper_z.set_sixteenth_step()
stepper_a.set_sixteenth_step()


# Move stepper
stepper_a.rotate(10)   ## CW
stepper_a.rotate(-10)	## CCW


stepper_z.rotate(10)	## Up
stepper_z.rotate(-10)	## Down
