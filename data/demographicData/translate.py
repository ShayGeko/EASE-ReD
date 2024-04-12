"""
creates a new csv file with translated data from the input csv file
using googletrans library
"""

import csv
import os
from googletrans import Translator

filename = "berlin.csv"
outputName = "berlin_translated.csv"

# input csv
filepath = os.path.join(os.path.dirname(__file__), filename)

# output csv
output_filepath = os.path.join(os.path.dirname(__file__), outputName)
translator = Translator()

with open(filepath, newline="", encoding="iso-8859-1") as csvfile, open(
    output_filepath, "w", newline="", encoding="utf-8"
) as outputfile:
    reader = csv.DictReader(csvfile)
    writer = csv.DictWriter(outputfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        for field, source in row.items():
            # src = source language, dest = destination language
            # view google translate docs for language codes
            result = translator.translate(source, src="de", dest="en")
            row[field] = result.text
            print(row[field])
        writer.writerow(row)
