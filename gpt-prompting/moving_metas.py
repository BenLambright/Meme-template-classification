import pandas as pd
import os
import pathlib

template_df = pd.read_csv("adjudicated_templates_trunc.csv")
BASE_PATH = pathlib.Path("/mnt/ssd/home/blambright/scraper_tests/dataset/all_images")
NEW_PATH = pathlib.Path("/mnt/ssd/home/blambright/template_selection")
for index, row in template_df.iterrows():
    template_name = row["meme_page_url"].split('/')[-1]
    template_path = BASE_PATH / template_name
    curr_path = NEW_PATH / row["Ontology"]
    os.makedirs(curr_path, exist_ok=True)
    for file in pathlib.Path(template_path).glob('*'):
        file.rename(curr_path / file.parts[-1])
