import json
import csv
import pandas as pd

def json_to_csv(json_file, csv_file):
    # Load the JSON file
    with open(json_file) as f:
        data = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Write to CSV
    df.to_csv(csv_file, index=False)

def csv_to_json(csv_file, json_file):
    # Load the CSV file
    df = pd.DataFrame(pd.read_csv(csv_file, sep = ","))

    # Convert to JSON
    df.to_json(json_file, orient="records")