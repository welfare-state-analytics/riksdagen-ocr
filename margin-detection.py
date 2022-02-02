import numpy as np
import os, json
import kblab
import requests
from requests.auth import HTTPBasicAuth
import cv2
from PIL import Image

with open(os.path.expanduser('~/credentials.txt'), 'r') as f:
	credentials = f.read()

# Iterate over filenames in the corpus
def api():
	response = requests.get(f"https://betalab.kb.se/prot-1974--128/prot_1974__128-064.jp2", auth=HTTPBasicAuth("demo", credentials))
	img = response.content
	with open("riksdagen-images/test.png", "wb") as f:
		f.write(img)

def preprocess():
	img = cv2.imread("riksdagen-images/test.png", cv2.IMREAD_GRAYSCALE)

	blur = cv2.GaussianBlur(img, (5,5), 0)
	cv2.imwrite("riksdagen-images/test-blur.png", blur)

	thresh, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	cv2.imwrite("riksdagen-images/test-otsu.png", otsu)

	thresh, blurotsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	cv2.imwrite("riksdagen-images/test-blurotsu.png", blurotsu)
#cv2.imshow('img', img)
#cv2.waitKey(0)

img = cv2.imread("riksdagen-images/test-blurotsu.png", cv2.IMREAD_GRAYSCALE)

nrows, ncols = img.shape
cols = (img == 255).sum(axis=0) > nrows * 0.9
rows = (img == 255).sum(axis=1) > ncols * 0.9
img = np.zeros((nrows, ncols), dtype=float)
img[rows] += 1
img[:,cols] += 1
img[img == 2] = 255
print(img.shape)
#img = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('img', img)
cv2.waitKey(0)


