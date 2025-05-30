from glob import glob
import os
import json
from uuid import UUID, uuid4

from tqdm import tqdm
import pandas as pd


DATADIR = "./data"
files = glob("*.json", root_dir=DATADIR)
rows = []
for file in tqdm(files):
    path = os.path.join(DATADIR, file)
    data = json.load(open(path))
    del data["start_finish"]
    del data["pts"]
    data["id"] = str(uuid4())
    data["dataset_id"], _ = os.path.splitext(file)
    rows.append(data)

df = pd.DataFrame(rows)
print(df)

CSVFILE = "tracks.csv"
df.to_csv(CSVFILE, index=False)
print("Saved to file", CSVFILE)
