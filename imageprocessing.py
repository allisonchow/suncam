from PIL import Image #accesses pillow library
import cv2
import numpy as np


"""
Binary image
"""


# Open image as PIL image object
img = Image.open('sky1.jpg')


# Create empty type 1 (grayscale) image object
bwimg = Image.new('1',img.size) 


# Create binary image. Iterate over every pixel in image.
for i in range(0,img.width):
	for j in range(0,img.height):

		# If red component is less than 0.8*255, then make pixel white
		if (img.getpixel((i,j))[0] < 204): 
			bwimg.putpixel((i,j), 0)
		
		# If red component is greater than 0.8*255, then make pixel black 
		else:
			bwimg.putpixel((i,j), 1)


# Save image
bwimg.save('binaryimage.jpg')


"""
Hough circle
"""


# Open image as cv2 object
bwimg = cv2.imread('binaryimage.jpg',0)


# Shrink image
rsimg = cv2.resize(bwimg, None, fx = 0.25, fy = 0.25)

cv2.imshow('Resized grayscale image',rsimg)	## Delete after testing


# Dilate image
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(100,100))	## Still figuring out what size to make kernels
dimg = cv2.dilate(rsimg,kernel,iterations=1)

cv2.imshow('Dilated image',dimg)	## Delete after testing


# Color conversion from grayscale to BGR
cimg = cv2.cvtColor(dimg,cv2.COLOR_GRAY2BGR)

cv2.imshow('BGR image',cimg)	## Delete after testing


# Find circles
circles = cv2.HoughCircles(dimg,cv2.HOUGH_GRADIENT,1,20,
							param1=50,param2=30,minRadius=0,maxRadius=0)


# Display circles and centers on resized grayscale image
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(rsimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(rsimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',rsimg)	## Delete after testing


# Display images	## Delete after testing
cv2.waitKey(0)
cv2.destroyAllWindows()
