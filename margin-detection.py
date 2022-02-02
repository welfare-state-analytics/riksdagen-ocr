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

# Preprocess image
original = cv2.imread("riksdagen-images/test.png")#, cv2.IMREAD_GRAYSCALE)
img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (5,5), 0)
thresh, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
thresh, blurotsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Detect margins
nrows, ncols = blurotsu.shape
cols = (blurotsu == 255).sum(axis=0) > nrows * 0.9
rows = (blurotsu == 255).sum(axis=1) > ncols * 0.9
blurotsu = np.zeros((nrows, ncols), dtype=np.uint8)
blurotsu[rows] += 255
blurotsu[:,cols] += 255
blurotsu[blurotsu == 255*2] = 255

# Fill boxes
contours, hierarchy = cv2.findContours(blurotsu.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img = np.zeros((nrows, ncols, 3), dtype=np.uint8)
cv2.fillPoly(img, pts=contours, color=(172,30,255))
img = cv2.addWeighted(img, 0.35, original, 0.5, 1.0)
cv2.imwrite("riksdagen-images/test-margin.png", img)

cv2.imshow('img', img)
cv2.waitKey(0)
