import pandas as pd

data = pd.read_csv("berlin.csv", sep=";", encoding="iso-8859-1")
data.drop(
    [
        "Bezirk",
        "Bez-Name",
        "Ortsteil",
        "Ortst-Name",
        "Geschl",
        "Altersgr",
        "Häufigkeit",
    ],
    axis=1,
    inplace=True,
)

data.to_csv("modifiedBerlin.csv", index=False)
