import pandas as pd
import numpy as np
import sys

file = sys.argv[1]
data = pd.read_csv(file)
filename = file.split("/")[-1].replace(".csv", "")
print(filename)

# can data, drop: Total - Gender_Symb	Men+ (2)	Men+_Symb	Women+ (3)	Women+_Symb
data = data.drop(data.columns[[0] + [2] + list(range(4, data.shape[1]))], axis=1)


charac = data.columns[0]
data[charac] = data[charac].str.strip()
data = data[~data[charac].str.startswith("Total")]

print(data)
data.to_csv(f"{filename}_cleaned.csv", index=False)
