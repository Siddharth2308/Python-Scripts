import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.VideoCapture(0)

while True:
    ret, frame = img.read()
    hImg, wImg, neglect = frame.shape
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    boxes = pytesseract.image_to_boxes(frame)

    for i in boxes.splitlines():
        i = i.split(' ')
        x,y,w,h = int(i[1]), int(i[2]), int(i[3]), int(i[4])
        cv2.rectangle(frame, (x, hImg - y), (w, hImg - h), (255,0,0), 1)
        cv2.putText(frame, i[0], (x, hImg - y + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)
    
    cv2.imshow("Output", frame)
    if cv2.waitKey(1) == ord('q'):
        break

img.release()
cv2.destroyAllWindows()

# img = cv2.imread('test.png')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# print(pytesseract.image_to_string(img))
# print(pytesseract.image_to_boxes(img))

# hImg, wImg, neglect = img.shape
# boxes = pytesseract.image_to_boxes(img)

# for b in boxes.splitlines():
#     b = b.split(' ')
#     x,y,w,h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
#     cv2.rectangle(img, (x, hImg - y), ( w, hImg - h), (255,0,0), 1)
#     cv2.putText(img, b[0], (x, hImg - y + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)

# cv2.imshow('Result', img)
# cv2.waitKey(0)