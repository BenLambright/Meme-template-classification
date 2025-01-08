import pandas as pd
import os
import time
import requests
from requests import HTTPError, RequestException, Timeout
adjudicated_df = pd.read_csv('adjudicated_all_trunc.csv')
for index, row in adjudicated_df.iterrows():
    attempts = 0
    while attempts < 10:
        try:
            response = requests.get(row["image_url"], timeout=2)
            time.sleep(1)
            data = response.content
            response.raise_for_status()
            # if we get to this point, presumably we have a successful download
            break
        except (ConnectionError, HTTPError, RequestException, Timeout) as err:
            attempts += 1
            time.sleep(1)
    # write image to both folders
    path_meta = "structured_data/meta/" + str(row["Ontology"])
    path_template = "structured_data/templates/" + row["other_link"].split('/')[-1] if isinstance(row["other_link"], str) else "structured_data/templates/" + "nan"
    os.makedirs(path_meta, exist_ok=True)
    os.makedirs(path_template, exist_ok=True)
    with open(os.path.join(path_meta, row["image_url"].split('/')[-1]), "wb") as f:
        f.write(data)
    with open(os.path.join(path_template, row["image_url"].split('/')[-1]), "wb") as f:
        f.write(data)
