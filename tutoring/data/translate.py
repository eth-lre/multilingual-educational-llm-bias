"""python -m src.data.translate.py data/raw/test_sampled.csv data/translated/test_fa.csv fa"""
from src.model.load_key import Azure_KEY_VAN as key
import requests
import uuid
import csv
from sys import argv
from tqdm import tqdm
from time import sleep
from .translate_params import *

# Add your key and endpoint
endpoint = "https://api.cognitive.microsofttranslator.com"

# Location, also known as region
location = "switzerlandnorth"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': [argv[-1]]
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4()),
}

# Read the source CSV file and provide the target CSV location
source_file = argv[1]
target_file = argv[2]
target_language = argv[3]

with open(source_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# Columns to translate
columns_to_translate = [
    'question', 'ground_truth', 'student_incorrect_solution'
]

# Translate the text in chunks


def translate_texts(texts):
    body = [{'text': text} for text in texts]
    request = requests.post(
        constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return [t['translations'][0]['text'] for t in response]

# Function to save the translated rows to the CSV file


def save_translated_rows(translated_rows, mode='w'):
    with open(target_file, mode, encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        if mode == 'w':  # Write header only if we're writing from the start
            writer.writeheader()
        writer.writerows(translated_rows)


# Initialize variables for batch processing
batch_size = 10
translated_rows = []

if end_idx==0:
    end_idx = len(rows)

# Read and translate in batches
for i in tqdm(range(start_idx, end_idx, batch_size)):
    batch_rows = rows[i:i + batch_size]
    for row in batch_rows:
        translated_row = row.copy()
        for column in columns_to_translate:
            text = row[column]
            translated_texts = translate_texts([text])
            translated_row[column] = translated_texts[0]
            sleep(5)  # To avoid hitting rate limits
        translated_rows.append(translated_row)
    save_translated_rows(translated_rows, mode='a' if i > 0 else 'w')
    translated_rows.clear()

# Ensure any remaining rows are written if the total number isn't a multiple of batch_size
if translated_rows:
    save_translated_rows(translated_rows, mode='a')
