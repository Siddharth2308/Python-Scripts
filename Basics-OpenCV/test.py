import numpy as np
import cv2
from collections import deque
from imutils.video import VideoStream
import argparse
import imutils
import time

src = None
erosion_size = 0
max_elem = 2
max_kernel_size = 21
title_trackbar_element_shape = 'Element:\n 0: Rect \n 1: Cross \n 2: Ellipse'
title_trackbar_kernel_size = 'Kernel size:\n 2n +1'
title_erosion_window = 'Erosion Demo'
title_dilation_window = 'Dilation Demo'


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE

'''
def erosion(val):
    erosion_size = cv2.getTrackbarPos(title_trackbar_kernel_size, title_erosion_window)
    erosion_shape = morph_shape(cv2.getTrackbarPos(title_trackbar_element_shape, title_erosion_window))
    
    element = cv2.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                       (erosion_size, erosion_size))
    
    erosion_dst = cv2.erode(frame, element)
    #cv2.imshow(title_erosion_window, erosion_dst)
'''

capture = cv2.VideoCapture(0)

sensitivity = 15
greenLower = np.array([0,0,255-sensitivity])
greenUpper = np.array([255,sensitivity,255])

pts = deque(maxlen=args["buffer"])

frame_rate_calc = 1
freq = cv2.getTickFrequency()


while True:
	ret, frame = capture.read()
	t1 = cv2.getTickCount()
	'''
	cv2.namedWindow(title_erosion_window)
	cv2.createTrackbar(title_trackbar_element_shape, title_erosion_window, 0, max_elem, erosion)
	cv2.createTrackbar(title_trackbar_kernel_size, title_erosion_window, 0, max_kernel_size, erosion)
        '''
	width = int(capture.get(3))
	height = int(capture.get(4))

	image = np.zeros(frame.shape, np.uint8)
	smaller_frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
	another_frame = cv2.GaussianBlur(smaller_frame, (11, 11), 0)
	hsv = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2HSV)
	hsv2 = cv2.cvtColor(another_frame, cv2.COLOR_BGR2HSV)
	lvu_frame = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2LAB)
	
	grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	(thresh, blackAndWhiteFrame) = cv2.threshold(grayFrame, 127, 255, cv2.THRESH_BINARY)

	blackAndWhiteFrame = cv2.GaussianBlur(blackAndWhiteFrame, (11, 11), 0)
	
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	blackAndWhiteFrame = cv2.bitwise_not(blackAndWhiteFrame)

	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		print(x,y)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10 and radius < 100:
			cv2.circle(smaller_frame, (int(x), int(y)), int(radius),
				(255, 0, 255), 2)
			cv2.circle(smaller_frame, center, 5, (255, 0, 255), -1)
	pts.appendleft(center)
	
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(smaller_frame, pts[i - 1], pts[i], (255, 0, 255), thickness)

	cv2.putText(smaller_frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
	#cv2.imshow('video bw', blackAndWhiteFrame)
	image[:height//2, :width//2] = smaller_frame
	image[height//2:, :width//2] = hsv2
	image[:height//2, width//2:] = another_frame
	image[height//2:, width//2:] = lvu_frame

	cv2.imshow('mask', mask)
	cv2.imshow('frame', image)

	t2 = cv2.getTickCount()
	time1 = (t2-t1)/freq
	frame_rate_calc= 1/time1

	if cv2.waitKey(1) == ord('q'):
		break

capture.release()
cv2.destroyAllWindows()
