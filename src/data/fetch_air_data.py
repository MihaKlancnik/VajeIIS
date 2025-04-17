import requests
from datetime import datetime
import xml.etree.ElementTree as ET

import yaml

def fetch_air_data():
    try:

        # Load configuration from YAML file
        params = yaml.safe_load(open("params.yaml"))["fetch"]

        url = params["url"]

        response = requests.get(url)
        response.raise_for_status()  

        file_path = "data/raw/air/air_data.xml"
        with open(file_path, "wb") as file:
            file.write(response.content)

        print(f"Fetching successful. Data saved to {file_path} at {datetime.now()}")

    except requests.RequestException as e:

        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_air_data()


#poetry run python src/data/preprocess_air_data.py 