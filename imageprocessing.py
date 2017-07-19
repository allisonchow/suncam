from PIL import Image #accesses pillow library
import cv2
import numpy as np


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
bwimg.save('binaryimage.png')


# Create cv2 image object
img = cv2.imread('binaryimage.png',0)


# Blurs image with 5x5 aperture size (unnecessary?)
# img = cv2.medianBlur(img,5)


# BGR to grayscale color conversion (unnecessary?)
# cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)


#
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()