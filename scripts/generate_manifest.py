import marimo

__generated_with = "0.19.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from glob import glob
    import os
    import json
    import hashlib

    from tqdm import tqdm
    import pandas as pd
    return glob, hashlib, json, os, pd, tqdm


@app.cell
def _(glob, hashlib, json, os, pd, tqdm):
    DATADIR = "./data"
    files = glob("*.json", root_dir=DATADIR)
    rows = []
    for file in tqdm(files):
        path = os.path.join(DATADIR, file)
        data = json.load(open(path))
        del data["start_finish"]
        del data["pts"]
        data["id"] = hashlib.md5(file.encode()).hexdigest()
        data["dataset_id"], _ = os.path.splitext(file)
        rows.append(data)

    df = pd.DataFrame(rows)
    print(df)

    CSVFILE = "tracks.csv"
    df.to_csv(CSVFILE, index=False)
    print("Saved to file", CSVFILE)
    return


if __name__ == "__main__":
    app.run()
