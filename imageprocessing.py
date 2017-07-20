"""
Uses solor systems and the mean to detect the center of the sun.
"Sun-tracking imaging system for intra-hour DNI forecasts" by Yinghao Chu, Mengying Li, Carlos F.M. Coimbra
"""


from PIL import Image
import cv2
import numpy as np
import colorsys



# Open bgr image
img_bgr = cv2.imread('sky1.jpg',1)


# Create hsv np array
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)		#  Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]


# Create grayscale image
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)	# Intensity (0-255)


# Create initial binary image
img_bin = img_gray



"""
b,g,r = img[0,0]
h,s,v = img_hsv[0,0]
intens = img_gray[0,0]

print "b,g,r {0}".format(intens)
"""

# Create empty type 1 (grayscale) image object
# bwimg = Image.new('1',img.size) 


# Image properties
row, col, ch = img_bgr.shape
d = img_bgr.dtype
print row,col ,ch,d



# Create binary image. Iterate over every pixel in image.
for x in range(0,row):
	for y in range(0,col):


		b = float(img_bgr.item(x,y,0))/255
		g = float(img_bgr.item(x,y,1))/255
		r = float(img_bgr.item(x,y,2))/255
		h = float(img_hsv.item(x,y,0))/179
		s = float(img_hsv.item(x,y,1))/255
		v = float(img_hsv.item(x,y,2))/255
		i = float(img_gray.item(x,y))/255


		F_8 = ((r+g+b+v+i)/5) - ((h+s)/2)

		img_bin.itemset(x, y, (F_8 > 0.1)*255)	# Set threshold to 0.85 empirically

		if x == 2566:
			if y == 907:
				print F_8

print b,g,r,h,s,v,i 



rsimg = cv2.resize(img_bin, None, fx = 0.25, fy = 0.25)
cv2.imshow('binary image', rsimg)
cv2.waitKey(0)
cv2.destroyAllWindows()






"""
# Save image
bwimg.save('binaryimage.jpg')
bwimg.show('binaryimage.jpg')



# Shrink image
rsimg = cv2.resize(bwimg, None, fx = 0.25, fy = 0.25)

cv2.imshow('Resized grayscale image',rsimg)	## Delete after testing
cv2.imwrite('rsimg.jpg',rsimg)

# Dilate image
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(100,100))	## Still figuring out what size to make kernels
dimg = cv2.dilate(rsimg,kernel,iterations=1)

cv2.imshow('Dilated image',dimg)	## Delete after testing
cv2.imwrite('dimg.jpg',dimg)

# Color conversion from grayscale to BGR
cimg = cv2.cvtColor(dimg,cv2.COLOR_GRAY2BGR)

cv2.imshow('BGR image',cimg)	## Delete after testing
cv2.imwrite('cimg.jpg',cimg)

# Find circles
circles = cv2.HoughCircles(dimg,cv2.HOUGH_GRADIENT,1,20,
							param1=50,param2=30,minRadius=0,maxRadius=0)


# Display circles and centers on resized grayscale image
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(rsimg,(i[0],i[1]),i[2],(255,0,0),2)
    # draw the center of the circle
    cv2.circle(rsimg,(i[0],i[1]),2,(0,255,0),3)

cv2.imshow('detected circles',rsimg)	## Delete after testing
cv2.imwrite('circles.jpg',rsimg)

# 


# Display images	## Delete after testing
cv2.waitKey(0)
cv2.destroyAllWindows()
"""