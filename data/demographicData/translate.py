import csv
import os
from googletrans import Translator
import sys


def translate_csv(filename, outputName):
    """
    Translates the content of a CSV file from German to English using Google Translate API.

    Args:
        filename (str): The name of the input CSV file.
        outputName (str): The name of the output translated CSV file.

    Returns:
        None
    """
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


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    translate_csv(input_file, output_file)
