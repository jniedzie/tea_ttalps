import re
from collections import defaultdict
import numpy as np


# category = "_Pat"
category = "_PatDSA"
# category = "_DSA"

FILE = f"../uncertainties_ANv3/uncertainties{category}.txt"

dimuon_sf_names = {
    "_Pat" : "PAT-PAT",
    "_PatDSA" : "PAT-DSA",
    "_DSA" : "DSA-DSA",
}
dimuon_sf_name = dimuon_sf_names[category]

# Map input names → LaTeX row names
NAME_MAP = {
    "luminosity": "Integrated luminosity",
    "PU": "PU SF",
    "IsoMu trigger": "Trigger SF",
    "muon reco": "PAT muon reco. SF",
    "muon tight ID": "PAT muon tight ID SF",
    "muon loose ID": "PAT muon loose ID SF",
    "muon tight Iso": "PAT muon tight Iso SF",
    "muon loose Iso": "PAT muon loose Iso SF",
    "DSA muon ID": "DSA muon reco",
    "DSA muon reco": "DSA muon ID SF",
    f"{dimuon_sf_name} Dimuon efficiency SF": "Dimuon SF",
    "Lxy uncertainty": "Dimuon \Lxy",
    "b-tagging": "\PQb tagging SF",
    "PU jet ID efficiency": "PU jet ID SF",
    "L1 Pre-firing": "L1 pre-firing",
    "JEC scale": "Jet energy scale",
    "JEC resolution": "Jet energy resolution",
    "MET JES uncertainty": "JES \ptmiss",
    "MET JER uncertainty": "JER \ptmiss",
    "MET unclustered energy": "\ptmiss unclustered energy",
}

eras = ["2016", "2017", "2018", "2022", "2023"]

# storage: data[era][row] = list of values
data = defaultdict(lambda: defaultdict(list))

current_era = None

# ---------- PARSE ----------
with open(FILE) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # detect era
        if line in eras:
            current_era = line
            continue

        # match "name  x  y  z"
        match = re.match(r"(.+?)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", line)
        if not match:
            continue

        name = match.group(1).strip()
        values = [float(x.replace(",", ".")) for x in match.groups()[1:]]

        if name in NAME_MAP:
            mapped = NAME_MAP[name]
            data[current_era][mapped].append(values)

# ---------- STATS ----------
def fmt(x):
    return "$<$ 0.1" if abs(x) < 0.05 else f"{x:.1f}"

def summarize(vals):
    if not vals:
        return ["-", "-", "-"]

    mins  = [v[0] for v in vals]
    maxs  = [v[1] for v in vals]
    means = [v[2] for v in vals]

    return [
        fmt(min(mins)),
        fmt(max(maxs)),
        fmt(np.mean(means)),
    ]

# ---------- ORDER FROM NAME_MAP ----------
rows = list(NAME_MAP.values())

# ---------- PRINT LATEX ----------
for row in rows:
    line = [row]
    for era in eras:
        vals = data[era].get(row, [])
        line.extend(summarize(vals))
    print(" & ".join(line) + r" \\")