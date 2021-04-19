import cv2

# cv2.IMREAD_COLOR : Loads a color image. It is the default fkag, signigfier : (-1)
# cv2.IMREAD_GRAYSCALE, signifier : (0)
# cv2.IMREAD_UNCHANGED : Loads image as such imcluding alpha channel, signifier : (1)
img = cv2.imread('assets/logo.jpg', 1)
img = cv2.resize(img, (0, 0), fx= 0.5, fy=0.5)
img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)

# cv2.imwrite('new_img.jpg', img)

cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()