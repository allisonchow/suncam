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


import cv2
import numpy as np


# Open bgr image
img_bgr = cv2.imread('sky_6.jpg',1)
b = np.array(img_bgr[:,:,0], dtype = float)/255
g = np.array(img_bgr[:,:,1], dtype = float)/255
r = np.array(img_bgr[:,:,2], dtype = float)/255


# Create hsv image
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)		#  Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
h = np.array(img_hsv[:,:,0], dtype = float)/179
s = np.array(img_hsv[:,:,1], dtype = float)/255
v = np.array(img_hsv[:,:,2], dtype = float)/255


# Create grayscale image
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)	# Intensity (0-255)
i = np.array(img_gray[:,:], dtype = float)/255


# Calculate threshold matrix
img_gray = ((r+g+b+v+i)/5 - (h+s)/2)*255


# Saturation below 0.023 become white
sat_023 = img_hsv[:,:,1]
sat_023[np.where(sat_023 < 0.023*255)] = 255


# If outside threshold, make black
img_gray[np.where(img_gray < 0.56*255)] = 0
img_gray[np.where(img_gray > 0.60*255)] = 0


# Max distance using Color Algorithm
row, col = np.nonzero(img_gray)
row_dist = row - np.mean(row)
col_dist = col - np.mean(col)
dist = np.sqrt(np.square(row_dist) + np.square(col_dist))
max_dist = np.mean(dist) + 0.1*np.std(dist)


# Location of white pixels in saturated image
row_sat, col_sat = np.nonzero(sat_023)
row_dist_sat = row_sat - np.mean(row_sat)
col_dist_sat = col_sat - np.mean(col_sat)
dist_sat = np.sqrt(np.square(row_dist_sat) + np.square(col_dist_sat))
max_dist_sat = np.mean(dist_sat) + 0.1*np.std(dist_sat)


# Remove pixels outside of standard deviation
for j in range(0,(len(dist_sat))):
	if dist_sat[j] > max_dist_sat:
		r = row_sat[j]
		c = col_sat[j]
		sat_023[r,c] = 0


cv2.imwrite("sky_6_sat_satmean.jpg", sat_023)


"""
# Find new center
row, col = np.nonzero(img_gray)
row_center = int(round(np.mean(row)))
col_center = int(round(np.mean(col)))


# Mark center
img_bgr = cv2.circle(img_bgr, (col_center, row_center), 10, (255,0,0),-1)



# Save images
#cv2.imwrite("sky_6 binary.jpg", img_gray)
#cv2.imwrite("sky_6 center.jpg", img_bgr)
"""



# Open images
img_gray = cv2.resize(img_gray, None, fx = 0.5, fy = 0.5)
img_bgr = cv2.resize(img_bgr, None, fx = 0.5, fy = 0.5)
sat_023 = cv2.resize(sat_023, None, fx = 0.5, fy = 0.5)
cv2.imshow("sat", sat_023)
#cv2.imshow("binary image", img_gray)
#cv2.imshow("original image", img_bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()

