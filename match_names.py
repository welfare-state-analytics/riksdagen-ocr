import os, re
import pandas as pd
from alto import parse_file
import progressbar

def main():
    pattern = "[A-ZÅÖÄ][a-zäöå]{2,12},? [A-ZÅÖÄ][a-zäöå]{2,12}( [A-ZÅÖÄ][a-zäöå]{2,12})?"
    e = re.compile(pattern)

    print("EXAMPLES:")
    print(e.match(" Matsson, Carl Johan"))
    print(e.match("Matsson, Carl Johan"))
    print(e.match("Matsson, Carl"))

    print(e.match("Matsson, CaRl Johan"))
    print(e.match("Matsson"))

    print("ACTUAL DATA:")
    folder = "altofiles/"
    altofiles = os.listdir(folder)
    altofiles = sorted(altofiles)
    print(altofiles[:25])

    d = {}

    ms = {}
    for altofile in progressbar.progressbar(altofiles):
        decade = altofile[3:].split("-")[0]
        fpath = folder + altofile
        alto = parse_file(fpath)
        words = alto.extract_words()
        text = " ".join(words)
        matches = e.finditer(text)

        starts = []
        ends = []
        names = []
        if matches is not None:
            for match in matches:
                start = match.start()
                end = match.end()
                matched_str = text[start:end]
                starts.append(start)
                ends.append(end)
                names.append(matched_str)

        starts.append(-1)

        inbetweens = zip(ends, starts[1:])
        inbetweens = [text[e:s] for e,s in inbetweens]

        m = {name: description for name, description in zip(names, inbetweens)}
        for name, description in m.items():
            if "f. " in description[:40]:
                d[decade] = d.get(decade, 0) + 1


        decade_m = ms.get(decade, {})
        for name, description in m.items():
            decade_m[name] = description
        ms[decade] = decade_m

    return ms

def to_df(ms):
    pattern = "f. [0-9]{4,4}"
    e = re.compile(pattern)


    pattern2 = ", [A-ZÅÖÄ][a-zäöå]{2,20},"
    e2 = re.compile(pattern2)

    rows = []
    municipalities = pd.read_csv("tatorter.csv")
    municipalities = set(municipalities["Tätort"])

    for decade in ms:
        for name, description in ms[decade].items():
            if "f. " in description[:40]:
                #print(name)#, description.split("Yttran")[0])

                match = e.search(description)
                #print(match)
                if match is not None:
                    year = int(match.group(0)[3:])
                    municipality = e2.search(description)

                    if municipality is None:
                        pass
                    else:
                        municipality = municipality.group(0).replace(",", "").strip()
                    row = [decade, name, year, municipality]

                    rows.append(row)

    df = pd.DataFrame(rows, columns=["decade", "name", "year", "municipality"])
    return df

if __name__ == '__main__':
    ms = main()
    df = to_df(ms)

    print(df)

    df.to_csv("mps.csv", index=False)