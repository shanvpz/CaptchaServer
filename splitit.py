import cv2
import numpy as np
import os
import sys
def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
 
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
 
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
 
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
 
	# return the list of sorted contours and bounding boxes
	return (cnts)


i = 0
file = sys.argv[1]
print("C:\\Users\\Administrator\\Desktop\\PyInvoice\\blobs\\input\\"+file)
image = cv2.imread(file)
#cv2.imshow('input image',image)
#cv2.waitKey(0)



gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


edged=cv2.Canny(gray,30,200)
#cv2.imshow('canny edges',edged)
#cv2.waitKey(0)


new = edged.copy()
contours, hierarchy=cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.imshow('canny edges after contouring', new)
#cv2.waitKey(0)



#print(contours)
print('Numbers of contours found=' + str(len(contours)))

contours = sort_contours(contours, method = "left-to-right")

for c in contours:
    if cv2.contourArea(c)>12:
        x,y,w,h=cv2.boundingRect(c)
        if w*h>150:       #old 80
            print(w*h)
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.imshow('Bounding rect',image)
            #cv2.waitKey(0)
            roi = image[y:y+h+1, x:x+w+1]
            cv2.imwrite('outs/test'+str(i)+'.jpg',roi)
            i=i+1
#cv2.waitKey(0)


#calculate accuracy as a percent of contour perimeter
#accuracy=0.01*cv2.arcLength(c,True)
#approx=cv2.approxPolyDP(c,accuracy,True)
#cv2.drawContours(image,[approx],0,(0,255,0),2)
#cv2.imshow('Approx polyDP', image)
#cv2.waitKey(0)
cv2.destroyAllWindows()



