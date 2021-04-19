import numpy as np
import cv2


capture = cv2.VideoCapture(0) #  here 0 will access the first cam 1 will access the second and so on

while True:
	ret, frame = capture.read()

	width = int(capture.get(3))
	height = int(capture.get(4))

	img = cv2.line(frame, (0,0), (width, height), (255,0,0), 10)
	img = cv2.line(img, (0,height), (width, 0), (0,255,0), 10)
	img = cv2.rectangle(img, (100,100), (200,200), (0,0,255), 5) # To fill pass -1 as an additional param
	img = cv2.circle(img, (300,300), 60, (0,0,255), -1)

	font = cv2.FONT_ITALIC
	img = cv2.putText(img, "Siddharth", (200, height-10), font, 4, (255,255,255), 5, cv2.LINE_AA)

	cv2.imshow('frame', img)

	if cv2.waitKey(1) == ord('q'):
		break

capture.release()
cv2.destroyAllWindows()