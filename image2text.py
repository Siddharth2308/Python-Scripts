import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR'
from PIL import Image

img = Image.open('test2.jpeg')
text = tess.image_to_string(img)
print(text)
