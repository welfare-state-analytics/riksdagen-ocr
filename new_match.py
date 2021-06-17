import alto

fpath = "altofiles/pr-1921-part-1-011.xml"
altofile = alto.parse_file(fpath)
tbs = altofile.extract_grouped_words("TextBlock")
paragraphs = [" ".join(tb) for tb in tbs]

# Print all paragraphs in a file
for paragraph in paragraphs:
    print(paragraph)
    print()
