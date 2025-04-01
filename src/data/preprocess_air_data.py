import numpy as np
import pandas as pd
from lxml import etree as ET

#def preprocess_air_data():
#    # Open XML file
#    with open("data/raw/air/air_data.xml", "rb") as file:
#        tree = ET.parse(file)
#        root = tree.getroot()
#
#    # Extract and print data
#    print(f"Version: {root.attrib['verzija']}")
#    print(f"Source: {root.find('vir').text}")
#    print(f"Suggested Capture: {root.find('predlagan_zajem').text}")
#    print(f"Suggested Capture Period: {root.find('predlagan_zajem_perioda').text}")
#    print(f"Preparation Date: {root.find('datum_priprave').text}")
#
#    sifra_vals = set(tree.xpath('//postaja/@sifra'))
#
#    postaja_elements = tree.xpath('//postaja[@sifra="E410"]')
#    
#    # Initialize an empty DataFrame
#    columns = ["Date_to", "PM10", "PM2.5"]
#    df = pd.DataFrame(columns=columns)
#
#    # Convert the XML data to a DataFrame
#    for postaja in postaja_elements:
#        date_to = postaja.find('datum_do').text
#        pm10 = postaja.find('pm10').text if postaja.find('pm10') is not None else np.nan
#        pm2_5 = postaja.find('pm2.5').text if postaja.find('pm2.5') is not None else np.nan
#
#        # Append the data as a new row in the DataFrame
#        df = pd.concat([df, pd.DataFrame([[date_to, pm10, pm2_5]], columns=columns)], ignore_index=True)
#
#    # Sort the DataFrame by the "date_to" column
#    df = df.sort_values(by="Date_to")
#    
#    # Replace string values
#    df = df.replace("", np.nan)
#    df = df.replace("<1", 1)
#    df = df.replace("<2", 2)
#    
#    # Save the DataFrame to a CSV file
#    df.to_csv("data/preprocessed/air/E410.csv", index=False)
#
#if __name__ == "__main__":
#    #parse_air_data()
#    preprocess_air_data()




#import os
#import numpy as np
#import pandas as pd
#from lxml import etree as ET
#
#def preprocess_air_data(station_id=None):
#    # Create directory if it doesn't exist
#    os.makedirs("data/preprocessed/air", exist_ok=True)
#    
#    # Open XML file
#    with open("data/raw/air/air_data.xml", "rb") as file:
#        tree = ET.parse(file)
#        root = tree.getroot()
#
#    # Extract and print metadata
#    print(f"Version: {root.attrib['verzija']}")
#    print(f"Source: {root.find('vir').text}")
#    print(f"Suggested Capture: {root.find('predlagan_zajem').text}")
#    print(f"Suggested Capture Period: {root.find('predlagan_zajem_perioda').text}")
#    print(f"Preparation Date: {root.find('datum_priprave').text}")
#
#    # Get all available station IDs if none specified
#    all_station_ids = set(tree.xpath('//postaja/@sifra'))
#    
#    # If no specific station ID is provided, process all stations
#    station_ids_to_process = [station_id] if station_id else all_station_ids
#    
#    for sifra in station_ids_to_process:
#        process_station(tree, sifra)
#    
#def process_station(tree, sifra):
#    print(f"Processing station ID: {sifra}")
#    
#    # Get all elements for the specific station
#    postaja_elements = tree.xpath(f'//postaja[@sifra="{sifra}"]')
#    
#    if not postaja_elements:
#        print(f"No data found for station ID: {sifra}")
#        return
#    
#    # Fixed columns - only date_to, pm10, and pm2.5
#    columns = ["date_to", "PM10", "PM2.5"]
#    df = pd.DataFrame(columns=columns)
#    
#    # Check if csv file already exists
#    output_path = f"data/preprocessed/air/{sifra}.csv"
#    if os.path.exists(output_path):
#        df = pd.read_csv(output_path)
#    
#    # Convert the XML data to a DataFrame
#    for postaja in postaja_elements:
#        # Extract date
#        date_to = postaja.find('datum_do').text
#        
#        # Extract only pm10 and pm2.5
#        pm10_element = postaja.find('pm10')
#        pm2_5_element = postaja.find('pm2.5')
#        
#        pm10 = pm10_element.text if pm10_element is not None else np.nan
#        pm2_5 = pm2_5_element.text if pm2_5_element is not None else np.nan
#        
#        # Append the data as a new row in the DataFrame
#        new_row = pd.DataFrame([[date_to, pm10, pm2_5]], columns=columns)
#        df = pd.concat([df, new_row], ignore_index=True)
#    
#    # Filter unique "datum_do" values
#    df = df.drop_duplicates(subset=["date_to"])
#    
#    # Sort the DataFrame by the "date_to" column
#    df = df.sort_values(by="date_to")
#    
#    # Replace string values
#    df = df.replace("", np.nan)
#    df = df.replace("<1", 1)
#    df = df.replace("<2", 2)
#    
#    # Save the DataFrame to a CSV file
#    df.to_csv(output_path, index=False)
#    print(f"Saved data for station {sifra} to {output_path}")
#
#if __name__ == "__main__":
#    # Process all stations
#    preprocess_air_data()


import os
import numpy as np
import pandas as pd
from lxml import etree as ET

def preprocess_air_data(station_id=None):
    # Create directory if it doesn't exist
    os.makedirs("data/preprocessed/air", exist_ok=True)
    
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

    # Get all available station IDs if none specified
    all_station_ids = set(tree.xpath('//postaja/@sifra'))
    
    # If no specific station ID is provided, process all stations
    station_ids_to_process = [station_id] if station_id else all_station_ids
    
    for sifra in station_ids_to_process:
        process_station(tree, sifra)
    
def process_station(tree, sifra):
    print(f"Processing station ID: {sifra}")
    
    # Get all elements for the specific station
    postaja_elements = tree.xpath(f'//postaja[@sifra="{sifra}"]')
    
    if not postaja_elements:
        print(f"No data found for station ID: {sifra}")
        return
    
    # Get all possible measurement types from the first station entry
    # This dynamically captures all available measurements
    first_station = postaja_elements[0]
    measurement_types = [child.tag for child in first_station 
                         if child.tag not in ['merilno_mesto', 'datum_od', 'datum_do']]
    
    # Initialize DataFrame columns
    columns = ["date_to"] + measurement_types
    df = pd.DataFrame(columns=columns)
    
    # Check if csv file already exists
    output_path = f"data/preprocessed/air/{sifra}.csv"
    if os.path.exists(output_path):
        df = pd.read_csv(output_path)
    
    # Convert the XML data to a DataFrame
    for postaja in postaja_elements:
        # Extract date
        date_to = postaja.find('datum_do').text
        
        # Extract all measurements
        row_data = [date_to]
        for measurement in measurement_types:
            element = postaja.find(measurement)
            value = element.text if element is not None else np.nan
            row_data.append(value)
        
        # Append the data as a new row in the DataFrame
        new_row = pd.DataFrame([row_data], columns=columns)
        df = pd.concat([df, new_row], ignore_index=True)
    
    # Filter unique "datum_do" values
    df = df.drop_duplicates(subset=["date_to"])
    
    # Sort the DataFrame by the "date_to" column
    df = df.sort_values(by="date_to")
    
    # Replace string values
    df = df.replace("", np.nan)
    df = df.replace("<1", 1)
    df = df.replace("<2", 2)
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False)
    print(f"Saved data for station {sifra} to {output_path}")

if __name__ == "__main__":
    # You can call with a specific station ID or without any to process all stations
    # Example: preprocess_air_data("E410")
    preprocess_air_data()


#poetry run python src/data/preprocess_air_data.py