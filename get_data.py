import json

#script to get names from top 500 artist JSON file and use those names to get their spotify data

with open("spotify_artists_data.json", encoding="utf-8") as file:
    data = json.load(file)

# Print just the top-level structure nicely
for i, (k, v) in enumerate(data.items()):
    print(f"{k}: {type(v)}")
    if i == 4:  # stop after 5 items
        break

print(data["x"][0])
