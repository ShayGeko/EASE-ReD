import csv 

# Open the csv file in read mode
with open('replace.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Skip the first column
    new_rows = [row[1:] for row in csv_reader]

# Open the csv file in write mode and overwrite it with the new data
with open('replace.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(new_rows)