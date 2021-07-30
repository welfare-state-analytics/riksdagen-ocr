from pyparlaclarin.read import paragraph_iterator
import os, re
import progressbar
from lxml import etree
import pandas as pd

pattern = "[A-ZÅÄÖÉ][a-zåäöéA-ZÅÄÖÉ]{2,20} i ([A-ZÅÄÖÉ][a-zåäöéA-ZÅÄÖÉ]{2,20}):"
exp = re.compile(pattern)

s = "Herr LARSSON i Hedenäset (cp)"

for m in exp.findall(s):
    print(m)

locations = []
pc_folder = "../riksdagen-corpus/corpus/"
folders = os.listdir(pc_folder)
parser = etree.XMLParser(remove_blank_text=True)
for outfolder in progressbar.progressbar(folders):
    if os.path.isdir(pc_folder + outfolder):
        outfolder = outfolder + "/"
        protocol_ids = os.listdir(pc_folder + outfolder)
        protocol_ids = [protocol_id.replace(".xml", "") for protocol_id in protocol_ids if protocol_id.split(".")[-1] == "xml"]

        for protocol_id in progressbar.progressbar(protocol_ids):
            filename = pc_folder + outfolder + protocol_id + ".xml"
            root = etree.parse(filename, parser).getroot()

            for paragraph in paragraph_iterator(root, output="lxml"):
                if paragraph.attrib.get("type") == "speaker":
                    paragraph = paragraph.text
                    for m in exp.findall(paragraph):
                        locations.append([m, outfolder])


df = pd.DataFrame(locations, columns=["place", "folder"])
df = df.drop_duplicates()
df = df.reset_index(drop=True)
df = df.sort_values("place")
print(df)
df.to_csv("locations.csv")
