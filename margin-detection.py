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

def preprocess_image(img):
	img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	img = cv2.GaussianBlur(img, (5,5), 0)
	_, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return img

def detect_margins(img, thresh_x=0.9, thresh_y=0.9):
	'''Detect margins (mark cells in row-column pairs which both have >0.9 white pixels)'''
	rows = (img == 255).sum(axis=1) > img.shape[1] * thresh_x
	cols = (img == 255).sum(axis=0) > img.shape[0] * thresh_y
	img = np.zeros(img.shape, dtype=img.dtype)
	img[rows] += 255
	img[:,cols] += 255
	img[img == 255*2] = 255
	return img

def detect_boxes(img):
	contours, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours[1:]

def merge_boxes(img, boxes, thresh_x=5):
	rects, rectsUsed, acceptedRects = [], [], []

	# Just initialize bounding rects and set all bools to false
	for cnt in cnts:
	    rects.append(cv2.boundingRect(cnt))
	    rectsUsed.append(False)
	rects.sort(key = lambda x: x[0])

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
	            if (candxMin <= currxMax + thresh_x):

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
	    img = cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (121, 11, 189), 2)
	return img

# Find boxes
img = preprocess_image(original)
img = detect_margins(img)
cnts = detect_boxes(img)
original = merge_boxes(original, cnts)
cv2.imshow('img', original)
cv2.waitKey(0)

