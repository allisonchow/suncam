"""
Use to reposition camera
"""


# Initialize Stepper
stepper_z = ed.easydriver("P8_7", 0.007, "P8_8")
stepper_a = ed.easydriver("P8_15", 0.007, "P8_16")



# Move stepper
stepper_z.rotate(180)
stepper_a.rotate(-15)