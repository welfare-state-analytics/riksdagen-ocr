import pandas as pd
import os
import sys
from pathlib import Path
import subprocess

years = pd.read_csv("metadata/statskalender_mop_pages.csv")
print(years)

p = Path(sys.argv[1])
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
			tess_command = ["tesseract", str(fname), "statscalender/" + plain_fname, "-l", "swe", "alto"]
			print(" ".join(tess_command))
			subprocess.call(tess_command)