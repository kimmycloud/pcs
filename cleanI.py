import csv

file = open ("output.txt", "r")

lines = file.readlines()
file.close()

gate_voltages = [] # list for VGS
sweeps = [] # list for all measurements


for line in lines:
    line = line.strip() # remove whitespace from beginning and end of line

    if line.startswith("GATE"):
        VGS = float(line.split()[-1])  # [-1] gets last element of list
        gate_voltages.append(VGS) # add VGS to list
        sweeps.append([]) # create new empty list for this sweep
        continue

    if line.startswith("VDS") or line == "":
        continue

    values = line.split()

    VDS = float(values[0])
    ID = float(values[1])

    sweeps[-1].append((VDS, ID)) # add (VDS, ID) tuple to last sweep


    file2 = open("output.csv", "w", newline="")
    writer = csv.writer(file2)

    headers = []

    for VGS in gate_voltages:
        headers.extend([f"VGS={VGS}", "VDS", "ID"])

    writer.writerow(headers)

    max_rows = 0

    for sweep in sweeps:
        if len(sweep) > max_rows:
            max_rows = len(sweep)

    for i in range(max_rows):
        row = []
        for sweep in sweeps:
            if i < len(sweep):
                VDS = sweep[i][0]
                ID = sweep[i][1]
                row.extend(["",VDS, ID])
            else:
                row.extend(["","", ""])  # fill with empty strings if no data
        writer.writerow(row)

file2.close()
from google.colab import files
files.download("output.csv")