import numpy as np
import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

#os.system('set -g TESSDATA_PREFIX ~/tesseract_data')

path = 'stadskalender_chamber_1'
files = [f for f in os.listdir(path)]

# Iterate files
file = files[0]

images = convert_from_path('/'.join([path, file]))

for image in images:
	s = pytesseract.image_to_string(image, lang='swe')
	print(s)

