import pandas as pd

# identifying all of the origins/ethnic groups in the Canada Census data
df = pd.read_csv("ethnicities_in_canadaCensus.csv")
unique = df.iloc[:, 0].unique()
df_unique = pd.DataFrame(unique, columns=[df.columns[0]])
df_unique.to_csv("ethnicities_in_canadaCensus.csv", index=False)
