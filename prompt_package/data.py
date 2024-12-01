import pandas as pd

# I'm getting my data from Jordan's annotated data because generally his annotations were more accurate, so this gives me gold data as well as image urls
jordans_data_path = "jordans_v4_annotations1.csv"

df = pd.read_csv(jordans_data_path)

data_dict = {row['caption']: (row['image'], row['Ontology']) for _, row in df.iterrows()}

# print(len(data_dict))