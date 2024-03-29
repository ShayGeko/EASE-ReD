import pandas as pd
import numpy as np
import sys

file = sys.argv[1]
data = pd.read_csv(file)
filename = file.split("/")[-1].replace(".csv", "")

# drop columns: Total - Gender_Symb	Men+ (2),	Men+_Symb,	Women+ (3),	Women+_Symb
data = data.drop(data.columns[[2] + list(range(4, data.shape[1]))], axis=1)

# remove columns that aren't the ethnic and total data
charac = data.columns[0]
total = data.columns[2]
data = data[data[charac] != "Visible minority"]
data = data[~data[charac].str.startswith("Total")]

data[charac] = data[charac].str.replace(r'["n.o.s.",,]', "", regex=True).str.strip()
data = data.drop(data.columns[0], axis=1)

# calculating the percentage for each group
data["percentage"] = data[total][1:] / data[total][1:].sum() * 100
data.to_csv(f"{filename}_cleaned.csv", index=False)
