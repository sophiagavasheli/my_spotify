import json
import csv
from access_spotify import get_artist, get_several_artists
import pandas as pd

#script to get names and spotify ids from top 500 artist JSON file and use those ids to get their spotify data

with open("spotify_artists_data.json", encoding="utf-8") as file:
    data = json.load(file)

# Extract 'i' and 'n' from each artist in data["x"], where i is id and n is name
artists = data["x"]

# Save to CSV
with open("artist_names_ids.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["spotify_id", "name"])  # Header row
    for artist in artists:
        writer.writerow([artist["i"], artist["n"]])

#get artist data
df = pd.read_csv("artist_names_ids.csv")
df["followers"] = ""
df["popularity"] = ""
df["genres"] = ""

df["spotify_id"] = df["spotify_id"].astype(str).str.strip()
    
# Chunk into groups of 50 and get artist data
batch_size = 50
for start in range(0, len(df), batch_size):
    end = start + batch_size
    batch_ids = df["spotify_id"].iloc[start:end].tolist()
    artists = get_several_artists(batch_ids)

    for artist in artists:
        artist_id = artist["id"]
        idx = df.index[df["spotify_id"] == artist_id][0]  # get index in DataFrame

        df.at[idx, "followers"] = artist["followers"]["total"]
        df.at[idx, "popularity"] = artist["popularity"]
        df.at[idx, "genres"] = ", ".join(artist["genres"])


# Save updated CSV
df.to_csv("artist_data.csv", index=False)