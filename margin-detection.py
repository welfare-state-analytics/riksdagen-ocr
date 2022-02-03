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
	with open("riksdagen-images/test0.png", "wb") as f:
		f.write(img)

# Preprocess image
original = cv2.imread("riksdagen-images/test0.png")#, cv2.IMREAD_GRAYSCALE)
img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (5,5), 0)
_, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
_, blurotsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Detect margins (mark cells in row-column pairs which both have >0.9 white pixels)
nrows, ncols = blurotsu.shape
cols = (blurotsu == 255).sum(axis=0) > nrows * 0.9
rows = (blurotsu == 255).sum(axis=1) > ncols * 0.9
blurotsu = np.zeros((nrows, ncols), dtype=np.uint8)
blurotsu[rows] += 255
blurotsu[:,cols] += 255
blurotsu[blurotsu == 255*2] = 255

# Find boxes
contours, _ = cv2.findContours(blurotsu.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Merge boxes
cnts = contours[1:] # First box is whole page
rects, rectsUsed, acceptedRects = [], [], []

# Just initialize bounding rects and set all bools to false
for cnt in cnts:
    rects.append(cv2.boundingRect(cnt))
    rectsUsed.append(False)
rects.sort(key = lambda x: x[0])

# Merge threshold for x coordinate distance
xThr = 5 # does not seem to do anything atm

# Iterate all initial bounding rects
for supIdx, supVal in enumerate(rects):
    if (rectsUsed[supIdx] == False):

        # Initialize current rect
        currxMin = supVal[0]
        currxMax = supVal[0] + supVal[2]
        curryMin = supVal[1]
        curryMax = supVal[1] + supVal[3]

        # This bounding rect is used
        rectsUsed[supIdx] = True

        # Iterate all initial bounding rects
        # starting from the next
        for subIdx, subVal in enumerate(rects[(supIdx+1):], start = (supIdx+1)):

            # Initialize merge candidate
            candxMin = subVal[0]
            candxMax = subVal[0] + subVal[2]
            candyMin = subVal[1]
            candyMax = subVal[1] + subVal[3]

            # Check if x distance between current rect
            # and merge candidate is small enough
            if (candxMin <= currxMax + xThr):

                # Reset coordinates of current rect
                currxMax = candxMax
                curryMin = min(curryMin, candyMin)
                curryMax = max(curryMax, candyMax)

                # Merge candidate (bounding rect) is used
                rectsUsed[subIdx] = True
            else:
                break

        # No more merge candidates possible, accept current rect
        acceptedRects.append([currxMin, curryMin, currxMax - currxMin, curryMax - curryMin])

for rect in acceptedRects:
    img = cv2.rectangle(original, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (121, 11, 189), 2)
#
#cv2.imwrite('riksdagen-images/test-final.png', original)
cv2.imshow('img', original)
cv2.waitKey(0)

