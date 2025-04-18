import requests
from bs4 import BeautifulSoup

def get_player_agent_stats(player_id: int, timespan: int = 30):
    timespan = timespan if timespan in [0, 30, 60, 90] else 60  # Default to 60 days if invalid timespan is provided
    url = "https://www.vlr.gg/player/" + str(player_id) + "/?timespan=" + ("all" if timespan == 0 else str(timespan)+"d") 
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(url, headers=headers)
        status = res.status_code
        res.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    except requests.exceptions.HTTPError as http_err:
        print(f"Error fetching products: {http_err}")
        return None
    except requests.exceptions.ConnectionError as errc:
        print("Connection error occurred:", errc)
        return None
    except requests.exceptions.Timeout as errt:
        print("Timeout error occurred:", errt)
        return None
    except requests.exceptions.RequestException as err:
        print("Some other error occurred:", err)    
        return None
        
    soup = BeautifulSoup(res.text, "lxml")

    # Get player name
    name = soup.find("h1", class_="wf-title").text.strip()

    # Extract career stats

    # Find the table with class="wf-table" inside the dark mod-table card
    try: 
        table = soup.find("div", class_="wf-card mod-table mod-dark").find("table", class_="wf-table")
    except AttributeError:
        print("Table not found")
        return None
    

    # Grab the table headers (th tags)
    headers = table.find("thead").find_all("th")[1:] # Skip the first column (agent name)
    # Extract text, clean up whitespace
    headers = [th.get_text(strip=True) for th in headers]
    headers.insert(0, "Agent")  # Add agent name to the headers
    rows = table.find_all("tr")[1:]
    agents = [] 
    stats = []

    # Iterate through each row in the table (skipping the header row)
    for i, row in enumerate(rows):
        agent = row.find("img").get("alt") if row.find("img") else "Unknown"
        agents.append(agent)
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
    data = {
        "name": name,
        "url": url,
        "current_stats": formatted_data
    }

    return {
        "status": status, 
        "data": data 
        }