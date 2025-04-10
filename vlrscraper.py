import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

id = "4004" # Zekken ID
url = "https://www.vlr.gg/player/" + id + "/?timespan=30d"
headers = {'User-Agent': 'Mozilla/5.0'}

res = requests.get(url, headers=headers)

# Catching errors
if res.status_code != 200:
    print(f"Error: {res.status_code}")
    exit()
    
soup = BeautifulSoup(res.text, "lxml")

# Get player name
name = soup.find("h1", class_="wf-title").text.strip()

# Extract career stats

stat_data = {}
# Find the table with class="wf-table" inside the dark mod-table card
table = soup.find("div", class_="wf-card mod-table mod-dark").find("table", class_="wf-table")

# Grab the table headers (th tags)
headers = table.find("thead").find_all("th")[1:] # Skip the first column (agent name)
# Extract text, clean up whitespace
headers = [th.get_text(strip=True) for th in headers]
headers.insert(0, "Agent")  # Add agent name to the headers
rows = table.find_all("tr")
agents = [] 
stats = []

# Iterate through each row in the table (skipping the header row)
for i, row in enumerate(table.find_all("tr")[1:]):
    agents.append(row.find("img").get("alt"))
    raw_stats = row.find_all("td")[1:]  # Skip the first column (agent name)
    # Extract text, clean up whitespace
    stats.append([stat.get_text(strip=True) for stat in raw_stats])

formatted_data = []

for i in range(len(agents)):
    row = {}
    row = dict(zip(headers[1:], stats[i]))
    row["Agent"] = agents[i]
    row_ordered = {key: row[key] for key in headers} # Reorder the dictionary to match the headers
    formatted_data.append(row_ordered)

# Prepare the full dictionary
player_data = {
    "name": name,
    "url": url,
    "current_stats": formatted_data
}

# Write to JSON file
with open("current_player_stats.json", "w", encoding="utf-8") as f:
    json.dump(player_data, f, indent=4)

print("Player stats saved to current_player_stats.json")
