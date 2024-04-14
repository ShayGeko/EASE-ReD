import csv


def replace_column_names():
    """
    This function is used to manipulate the 'replace.csv' file by removing the first column
    and saving the modified content back to the same file. The purpose is to replace the column
    names in each Canada census CSV file with their country name instead of 'Place of Origin'.
    """

    with open("replace.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        new_rows = [row[1:] for row in csv_reader]

    with open("replace.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(new_rows)


if __name__ == "__main__":
    replace_column_names()
