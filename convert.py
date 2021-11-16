"""
OCR specific pages with tesseract.
Takes in a folder of PDFs, converts them into images, and OCRs the
pages mentioned in read
"""
import pandas as pd
import os
import sys
from pathlib import Path
import subprocess
import argparse

def main(args):
	years = pd.read_csv(args.csv_path)
	print(years)

	p = Path(args.infolder)
	for _, row in years.iterrows():
		start = row["start_page"]
		end = row["end_page"]
		command = "pdfimages -png "
		command = command + "-f " + str(start) + " -l " + str(end) + " "

		files = list(p.glob("*" + str(row["year"]) + ".pdf"))
		
		if len(files) > 0:
			plainname = str(files[0]).split("/")[-1].split(".")[0]
			command = command + str(files[0]) + " "
			command = command + " " + "images/" + plainname
			print(command)
			subprocess.call(command.split())

			p1 = Path("images/")

			for fname in p1.glob("*.png"):
				plain_fname = str(fname).split(".")[0].split("/")[-1]
				tess_command = ["tesseract", str(fname), args.outfolder + plain_fname, "-l", "swe", "alto"]
				print(" ".join(tess_command))
				subprocess.call(tess_command)

			for fname in p1.glob("*.png"):
				subprocess.call(["rm", str(fname)])

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--infolder", type=str, default="pdfs/")
	parser.add_argument("--csv_path", type=str, default="metadata/statskalender_mop_pages.csv")
	parser.add_argument("--outfolder", type=str, default="statscalender/")
	args = parser.parse_args()

	main(args)