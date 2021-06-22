import os, re
import pandas as pd
from alto import parse_file
import progressbar

def main():
    name = "[A-ZÅÖÄÉ][a-zäöåéA-ZÅÄÖ\\-]{2,25}"
    opt_name = "( " + name + ")?"
    born = "f\\. [0-9]{4,4}" # Born eg. f. 1929
    pattern = name + ", " + name + opt_name + opt_name + "[\S  ]{0,25}" + born
    print(pattern)
    e = re.compile(pattern)

    print("EXAMPLES:")
    print(e.match("Matsson, Carl Johan sdds f. 1234"))
    print(e.match("Matsson, Carl Johan, f. 1234"))
    print(e.match("Matsson, Carl-Johan, f. 1234"))
    print(e.match("MATSSON, Carl Johan, f. 1234"))
    print(e.match("Matsson, Carl Magnus Isak i dssdd f. 1234"))

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
            if len(name.split()[0]) <= 1:
                name = name[2:]
            decade_m[name] = description
        ms[decade] = decade_m

    return ms

def to_df(ms):
    pattern = "f. [0-9]{4,4}"
    e = re.compile(pattern)

    pattern2 = " [A-ZÅÖÄ][a-zäöå]{2,20},"
    e2 = re.compile(pattern2)

    rows = []
    municipalities = pd.read_csv("tatorter.csv")
    municipalities = set(municipalities["Tätort"])

    name = "[A-ZÅÖÄ][a-zäöåA-ZÅÄÖ\\-]{2,25}"
    opt_name = "( " + name + ")?"
    namepattern = name + ", " + name + opt_name + opt_name
    eName = re.compile(namepattern)

    locations = pd.read_csv("locations.csv")["Location"]
    locations = set(locations)

    for decade in ms:
        for name, description in ms[decade].items():
            #if "f. " in description[:40]:
            #print(name)#, description.split("Yttran")[0])

            match = e.search(name)
            description = description.replace(" | ", " ")
            description = description.replace("- ", "")
            #print(match)

            if "almkvist" in name.lower():
                print(name)
                print(description)
                print()

            namematch = eName.search(name)

            if match is not None and namematch is not None:
                year = int(match.group(0)[3:])
                municipality = None
                for m in e2.finditer(description):
                    m = m.group(0).replace(",", "").strip()

                    if m in locations:#m != "Johannesnäs":
                        municipality = m
                        break

                name = namematch.group(0)
                capitalized_name = name.lower().split()
                capitalized_name = " ".join(["-".join([w.capitalize() for w in wd.split("-")])
                    for wd in capitalized_name])

                row = [decade, capitalized_name, year, municipality]

                rows.append(row)

    df = pd.DataFrame(rows, columns=["decade", "name", "year", "municipality"])
    return df

if __name__ == '__main__':
    ms = main()
    df = to_df(ms)

    print(df)

    df.to_csv("mps.csv", index=False)