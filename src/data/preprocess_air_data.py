import os
import yaml
import numpy as np
import pandas as pd
from lxml import etree as ET

def preprocess_air_data():
    # Load configuration from YAML file
    params = yaml.safe_load(open("params.yaml"))["preprocess"]

    # Open XML file
    with open("data/raw/air/air_data.xml", "rb") as file:
        tree = ET.parse(file)
        root = tree.getroot()

    # Extract and print metadata
    print(f"Version: {root.attrib['verzija']}")
    print(f"Source: {root.find('vir').text}")
    print(f"Suggested Capture: {root.find('predlagan_zajem').text}")
    print(f"Suggested Capture Period: {root.find('predlagan_zajem_perioda').text}")
    print(f"Preparation Date: {root.find('datum_priprave').text}")

    # Get all station codes
    all_station_ids = set(tree.xpath('//postaja/@sifra'))

    # Use specific station from YAML, or process all if not specified
    station_id = params.get("station", None)
    station_ids_to_process = [station_id] if station_id else all_station_ids

    for sifra in station_ids_to_process:
        if sifra not in all_station_ids:
            print(f"Skipping invalid station code: {sifra}")
            continue
        process_station(tree, sifra)

def process_station(tree, sifra):
    print(f"Processing station ID: {sifra}")
    
    postaja_elements = tree.xpath(f'//postaja[@sifra="{sifra}"]')
    if not postaja_elements:
        print(f"No data found for station ID: {sifra}")
        return

    columns = ["date_to", "PM10", "PM2.5"]
    df = pd.DataFrame(columns=columns)

    output_path = f"data/preprocessed/air/{sifra}.csv"
    if os.path.exists(output_path):
        print(f"File already exists: {output_path}")
        df = pd.read_csv(output_path)
        print("Loaded existing DataFrame:\n", df.head())

    for postaja in postaja_elements:
        date_to = postaja.find('datum_do').text
        pm10 = postaja.find('pm10').text if postaja.find('pm10') is not None else np.nan
        pm2_5 = postaja.find('pm2.5').text if postaja.find('pm2.5') is not None else np.nan
        df = pd.concat([df, pd.DataFrame([[date_to, pm10, pm2_5]], columns=columns)], ignore_index=True)

    df = df.drop_duplicates(subset=["date_to"])
    df = df.sort_values(by="date_to")
    df = df.replace("", np.nan).replace("<1", 1).replace("<2", 2)

    os.makedirs("data/preprocessed/air", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved data to {output_path}")

if __name__ == "__main__":
    preprocess_air_data()
