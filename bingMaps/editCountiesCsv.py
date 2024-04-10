import pandas as pd

# Load the data
df = pd.read_csv(
    "counties_states.csv",
    header=None,
)

# Merge two columns together with a space in between
newDf = df[df.columns[0]].astype(str) + " " + df[df.columns[1]].astype(str)

# Write it back to a new file
newDf.to_csv(
    "edited_counties.csv",
    header=False,
    index=False,
)
