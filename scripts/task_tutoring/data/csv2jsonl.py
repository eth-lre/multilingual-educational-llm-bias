import csv
import json
import os
import glob

def csv_to_jsonl(csv_file_path, jsonl_file_path):
    with open(csv_file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open(jsonl_file_path, mode='w') as jsonl_file:
            for row in csv_reader:
                jsonl_file.write(json.dumps(row) + '\n')


# Directory containing the CSV files
directory_path = 'data/translated/'
print(os.listdir(directory_path))

# Get all files in the directory that match the pattern "test_<2 letter language code>.csv"
csv_files = [f for f in glob.glob(os.path.join(directory_path, 'test_??.csv')) if os.path.isfile(f)]
print(csv_files)

# Convert each matching CSV file to JSONL
for csv_file_path in csv_files:
    jsonl_file_path = csv_file_path.replace('.csv', '.jsonl').replace('translated', 'processed')
    csv_to_jsonl(csv_file_path, jsonl_file_path)
