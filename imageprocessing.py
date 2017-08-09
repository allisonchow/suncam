"""
Uses saturation values of the image to create binary image.
Uses clustering functions to find center of the sun.
"""


import numpy as np
import cv2
from pylab import *
from scipy.ndimage import measurements


def sun_center(img):

	"""
	Find the center of the sun and its distance to the center of the image.

	Parameters
    ----------
    img : string 
		The timestamp of the image taken by the suncam in the format, ts.strftime("%Y%m%d_%H%M%S")

    Returns
    -------
    dist_x : float
		Number of pixels in the x-direction between sun center and image center

    dist_y : float
    	Number of pixels in the y-direction between sun center and image center    	
	"""


	# Open bgr image
	img_bgr = cv2.imread("/home/suncam/fswebcampics/{0}.jpg".format(img),1)
	row, col, ch = np.shape(img_bgr)
	b = np.array(img_bgr[:,:,0], dtype = float)/255
	g = np.array(img_bgr[:,:,1], dtype = float)/255
	r = np.array(img_bgr[:,:,2], dtype = float)/255


	# Create hsv image
	img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)		#  Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
	h = np.array(img_hsv[:,:,0], dtype = float)/179
	s = np.array(img_hsv[:,:,1], dtype = float)/255


	# Create new image
	img_sun = np.full((row, col), 255, dtype = float)


	# If within threshold, make black
	img_sun[np.where((r > 0.96) & (g > 0.96) & (b > 0.96) & (s > 0.027) & (h > 0.8))] = 0


	# Label clusters
	lw, num = measurements.label(img_sun)

	# Find area of clusters
	area = measurements.sum(img_sun, lw, index=arange(len(lw)))
	area[np.where(area == np.amax(area))] = 0

	# Find center of mass
	[com_row, com_col] = np.round(measurements.center_of_mass(img_sun, lw, np.argmax(area)))
	dist_y = row/2 - com_row	# Positive difference = above true center(move down); Negative difference = below true center (move up) 
	dist_x = com_col - col/2	# Positive difference = right of true center (move left); Negative difference = left of true center (move right)
	# dist_abs = sqrt(pow(dist_x, 2) + pow(dist_y, 2))


	# Mark center (Delete after testing)
	img_bgr = cv2.line(img_bgr, (np.int(com_col + 1 - 10), np.int(com_row + 1)), (np.int(com_col + 1 + 10), np.int(com_row + 1)), [255,0,0], 1, 8)
	img_bgr = cv2.line(img_bgr, (np.int(com_col + 1), np.int(com_row + 1 - 10)), (np.int(com_col + 1), np.int(com_row + 1 + 10)), [255,0,0], 1, 8)


	# Save image
	cv2.imwrite('/home/suncam/fswebcampics/{0} Center.jpg'.format(img), img_bgr)	# Delete after testing
	cv2.imwrite('/home/suncam/fswebcampics/{0} Binary.jpg'.format(img), img_sun)	# Delete after testing


	# Return values
	return [dist_x, dist_y]


def rotate_center(dist_x, dist_y):
	"""
	Rotate the stepper motors the distance between the sun center and the image center.
	
	Uses basic trigonometric relationships to solve for the degree-pixel relationship:

	theta = 0.5*HFOV
	b = number of pixels across
	l = distance to center of image (cancels out)
	x = offset of pixels from sun center to image center
	phi = angle to rotate

	tan(theta) = (b/2)/l
	tan(phi) = x/l
	... phi = arctan((2xtan(theta))/b)

	Webcam (Logitech C270) Specs
	----------------------------
	FOV = 58 degrees
	HFOV = 58
	VFOV = (1080/1920)*FOV = 32.625

	Parameters
    ----------
    dist_x : float
		Number of pixels in the x-direction between sun center and image center

   	dist_y : float
    	Number of pixels in the y-direction between sun center and image center  

    Returns
    -------
	"""


	if dist_x > thresh:
	    
	    # Calculate degrees to rotate
	    degree_a = -math.degrees(math.atan(2*dist_x*math.tan(58/2)/1920))
	    
	    # Rotate motor
	    degree_a = stepper_a.rotate(degree_a)


	elif:

		degree_a = 0


    if dist_y > thresh:

        # Calculate degrees to rotate
	    degree_z = math.degrees(math.atan(2*dist_y*math.tan(32.625/2)/1080))

	    # Rotate motor
	    degree_z = stepper_z.rotate(degree_z)


	elif:

		degree_z = 0


	return [degree_a, degree_z]
