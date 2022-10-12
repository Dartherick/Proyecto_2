#https://stackoverflow.com/questions/65744862/area-of-a-closed-contour-on-a-plot-using-python-opencv

import cv2
import numpy as np

# read image as grayscale
img = cv2.imread('closed_curve.jpg')

# convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#select blu color range in hsv
lower = (24,128,115)
upper = (164,255,255)

# threshold on blue in hsv
thresh = cv2.inRange(hsv, lower, upper)

# get largest contour
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = contours[0] if len(contours) == 2 else contours[1]
big_contour = max(contours, key=cv2.contourArea)
area = cv2.contourArea(big_contour)
print("Area =",area)

# draw filled contour on black background
result = np.zeros_like(thresh)
cv2.drawContours(result, [big_contour], -1, 255, cv2.FILLED)

# view result
cv2.imshow("threshold", thresh)
cv2.imshow("result", result)

cv2.waitKey(0)
cv2.destroyAllWindows()
