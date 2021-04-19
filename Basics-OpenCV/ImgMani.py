import cv2
import random

img = cv2.imread('assets/logo.jpg', 1)
img = cv2.resize(img, (0, 0), fx= 0.5, fy=0.5)

for i in range(100):
	for j in range(img.shape[1]):
		img[i][j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]



# print(img[257][400])
# print(img.shape)

cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()