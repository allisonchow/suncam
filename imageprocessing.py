"""
Uses saturation values of the image to create binary image.
Uses clustering functions to find center of the sun.
"""


import numpy as np
import cv2
from pylab import *
from scipy.ndimage import measurements
import math


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

    check : float
    	Equals 0 if sun center is not detected. Equals 1 if sun center is detected.  	
	"""

	# Set checkmark value
	check = 0	# If 1, then sun center detected. If 0, then sun center not detected
	x = [0.021, 0.018, 0.012, 0.008]	# list of threshold values to check
	i = 0

	# Open image
	img_bgr = cv2.imread("/home/suncam/fswebcampics/{0}.jpg".format(img),1)
	row, col, ch = np.shape(img_bgr)

	# Extract color values
	b = np.array(img_bgr[:,:,0], dtype = float)/255
	g = np.array(img_bgr[:,:,1], dtype = float)/255
	r = np.array(img_bgr[:,:,2], dtype = float)/255

	img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)		#  Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
	h = np.array(img_hsv[:,:,0], dtype = float)/179
	s = np.array(img_hsv[:,:,1], dtype = float)/255


	# Create empty image array
	img_sun = np.full((row, col), 255, dtype = float)

	while check == 0:

		j = x[i]

		# If within threshold, make black
		img_sun[np.where((r > 0.96) & (g > 0.96) & (b > 0.96) & (h > 0.78) & (s > j))] = 0


		cv2.imwrite('/home/suncam/fswebcampics/{0} Binary THRESH {1}.jpg'.format(img,j), img_sun)	# Delete after testing


		# Label clustersd
		lw, num = measurements.label(img_sun)

		# Makes sure that clusters are detected
		if num > 1:

			# Find area of clusters
			area = measurements.sum(img_sun, lw, index=arange(len(lw)))
			area[np.where(area == np.amax(area))] = 0

			# Makes sure that detected clusters are correct
			if area[np.argmax(area)] > 50000:

				# Find center of mass
				[com_row, com_col] = np.round(measurements.center_of_mass(img_sun, lw, np.argmax(area)))
				dist_y = row/2 - com_row	# Positive difference = above true center(move down); Negative difference = below true center (move up) 
				dist_x = com_col - col/2	# Positive difference = right of true center (move left); Negative difference = left of true center (move right)
				# dist_abs = sqrt(pow(dist_x, 2) + pow(dist_y, 2))

				# Mark center (Delete after testing)
				img_bgr = cv2.line(img_bgr, (np.int(com_col + 1 - 10), np.int(com_row + 1)), (np.int(com_col + 1 + 10), np.int(com_row + 1)), [255,0,0], 1, 8)
				img_bgr = cv2.line(img_bgr, (np.int(com_col + 1), np.int(com_row + 1 - 10)), (np.int(com_col + 1), np.int(com_row + 1 + 10)), [255,0,0], 1, 8)

				cv2.imwrite('/home/suncam/fswebcampics/{0} Center THRESH {1}.jpg'.format(img,j), img_bgr)	# Delete after testing

				check = 1


			else:
				#print ('Sun center not detected at {0}. Area too small. THRESH {1}'.format(img,j))
				if j == 0.008:
					check = 2

		else:
			#print ('Sun center not detected at {0}. Not enough clusters detected. THRESH {1}'.format(img,j))
			if j == 0.008:
				check = 2

		i += 1


	# Return values
	return [dist_x, dist_y, check]


def rotate_center(dist_x, dist_y):
	"""
	
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
    degree_a : float
    	Number of degrees for azimuthal stepper to rotate

    degree_z : float
    	Number of degrees for zenith stepper to rotate
	"""
	    
    # Calculate azimuthal degrees to rotate
	degree_a = math.degrees(math.atan(2*dist_x*math.tan(58/2)/1920))

    # Calculate zenith degrees to rotate
	degree_z = math.degrees(math.atan(2*dist_y*math.tan(32.625/2)/1080))

	return [degree_a, degree_z]