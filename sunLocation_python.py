from PIL import Image
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm

img = cv2.imread('sky1.jpg')
print img.shape

#normalize blue, green, red pixels
b = (np.array(img[:, :, 0], dtype=float))/255 #note: index of arrays starts with 0 in python
g = (np.array(img[:, :, 1], dtype=float))/255
r = (np.array(img[: ,:, 2], dtype=float))/255

#convert rgb pixels to hsv and normalize
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h = (np.array(hsv[:, :, 0], dtype=float))/179
s = (np.array(hsv[:, :, 1], dtype=float))/255
v = (np.array(hsv[: ,:, 2], dtype=float))/255

#convert rgb pixels to greyscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
i = (np.array(gray[:, :], dtype=float))/255

#subtract avg of hue,saturation from avg of rgb,value,illuminance
av_rgbvi = (r+g+b+v+i)/5
av_hs = (h+s)/2
FF8 = av_rgbvi - av_hs
thres = 0.85 #threshold

#F8 true where FF8 greater than a certain threshold value
F8 = FF8 > (thres*np.amax(FF8)) 
print F8.shape

if F8.any() == True: #if FF8 > threshold, find its row & col indices
    row, col = np.where(F8)

#find median index of row and column pixel
mrow = np.median(row) 
mcol = np.median(col)
print '\n', mrow, mcol

#distance to mean location where: distance = sqrt(x^2 + y^2)
dis = np.sqrt(np.square(row - mrow) + np.square(col - mcol)) 
##print '\n', dis
sigrow = np.std(row) #standard deviation of row & col
sigcol = np.std(col)
dis_max = np.sqrt(np.square(sigrow) + np.square(sigcol)) #distance to mean location
print '\n', dis_max 

#Delete distances larger than max distance, i.e. outsider points
outsiders = dis > dis_max
if outsiders.any() == True:
    index = np.where(outsiders)
    ##print index
    for i in index:
        outsiders = np.delete(outsiders, i)
        dis = np.delete(dis, i)
        row = np.delete(row, i)
        col = np.delete(col,i)
        print row, col
                
#Sunlocation
Sunr = np.average(row, axis=0)
Sunc = np.average(col, axis=0)
SunL = [round(Sunr), round(Sunc)]
print SunL

