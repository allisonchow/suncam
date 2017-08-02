"""
Uses solor systems and the mean to detect the center of the sun.
"Sun-tracking imaging system for intra-hour DNI forecasts" by Yinghao Chu, Mengying Li, Carlos F.M. Coimbra

Helpful image processing link:
http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html

1-clear
2-small cloud
3-wispy clouds
4-cloudy
5-very cloudy
"""



import numpy as np
import cv2
from pylab import *
from scipy.ndimage import measurements


def sun_center(img):

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
	dist_row = row/2 - com_row	# Positive difference = above true center(move down); Negative difference = below true center (move up) 
	dist_col = com_col - col/2	# Positive difference = right of true center (move left); Negative difference = left of true center (move right)
	dist_abs = sqrt(pow(dist_row, 2) + pow(dist_col, 2))


	# Mark center
	img_bgr = cv2.line(img_bgr, (np.int(com_col + 1 - 10), np.int(com_row + 1)), (np.int(com_col + 1 + 10), np.int(com_row + 1)), [255,0,0], 1, 8)
	img_bgr = cv2.line(img_bgr, (np.int(com_col + 1), np.int(com_row + 1 - 10)), (np.int(com_col + 1), np.int(com_row + 1 + 10)), [255,0,0], 1, 8)


	# Save image
	cv2.imwrite('{0} Center.jpg'.format(img), img_bgr)
	cv2.imwrite('{0} Binary.jpg'.format(img), img_sun)


	# Return values
	return [dist_row, dist_col, dist_abs]
