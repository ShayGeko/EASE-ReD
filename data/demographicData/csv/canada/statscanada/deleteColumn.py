import csv

# made for manipulating the replace.csv file to replace the column names in each Canada census csv
# file with their country name instead of Place of Origin
with open("replace.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    new_rows = [row[1:] for row in csv_reader]

with open("replace.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(new_rows)
