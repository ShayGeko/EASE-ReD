import sys
import pandas as pd
import numpy as np

def main(input):
    #format:
    # header
    # "ab", "bc", "de" 
    df = pd.read_csv(input, sep = ",")

    print(df.head())

if __name__ == "__main__":
    input = sys.argv[1]

    main(input)