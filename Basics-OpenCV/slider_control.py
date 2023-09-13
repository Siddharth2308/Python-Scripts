import cv2
import numpy as np

# Function to update the image based on slider values
def update_image(*args):
    global modified_image
    hue_shift = cv2.getTrackbarPos('Hue', 'Parameters')
    saturation = cv2.getTrackbarPos('Saturation', 'Parameters')
    blur_size = cv2.getTrackbarPos('Blur Size', 'Parameters')
    erode_size = cv2.getTrackbarPos('Erode Size', 'Parameters')
    dilate_size = cv2.getTrackbarPos('Dilate Size', 'Parameters')

    # Adjust hue and saturation
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_shift) % 360
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] + saturation, 0, 255)
    modified_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Apply Gaussian blur
    modified_image = cv2.GaussianBlur(modified_image, (blur_size * 2 + 1, blur_size * 2 + 1), 0)

    # Apply erosion and dilation
    kernel = np.ones((erode_size * 2 + 1, erode_size * 2 + 1), np.uint8)
    modified_image = cv2.erode(modified_image, kernel, iterations=1)
    kernel = np.ones((dilate_size * 2 + 1, dilate_size * 2 + 1), np.uint8)
    modified_image = cv2.dilate(modified_image, kernel, iterations=1)

    cv2.imshow('Modified Image', modified_image)

# Load the image
image = cv2.imread('logo.jpg')  # Replace 'your_image.jpg' with the path to your image

# Create a window for parameter adjustments
cv2.namedWindow('Parameters')

# Create trackbars for hue, saturation, Gaussian blur, erosion, and dilation
cv2.createTrackbar('Hue', 'Parameters', 0, 360, update_image)
cv2.createTrackbar('Saturation', 'Parameters', 0, 255, update_image)
cv2.createTrackbar('Blur Size', 'Parameters', 0, 10, update_image)
cv2.createTrackbar('Erode Size', 'Parameters', 0, 10, update_image)
cv2.createTrackbar('Dilate Size', 'Parameters', 0, 10, update_image)

# Initialize the modified image
modified_image = np.copy(image)

# Display the original image
cv2.imshow('Original Image', image)

# Call update_image to initialize the modified image
update_image()

# Wait for a key press and then close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()
