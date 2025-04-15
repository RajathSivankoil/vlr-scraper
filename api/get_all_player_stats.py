import requests
from bs4 import BeautifulSoup
from api.save_to_json import save_to_json

# This function scrapes player statistics for VCT 2025 for a specified region and timespan.
# Much of this function was taken from the VLR API made by axsddlr on GitHub.
def get_all_player_stats(region: str, timespan: int):
    
    timespan = timespan if timespan in [0, 30, 60, 90] else 60  # Default to 60 days if invalid timespan is provided
    headers = {"User-Agent": "Mozilla/5.0"} 
    url = f"https://www.vlr.gg/stats/?event_group_id=74&region={region}&min_rounds=0&min_rating=1550&agent=all&map_id=all" + "&timespan=" + ("all" if timespan == 0 else str(timespan)+"d") 

    try:
        res = requests.get(url, headers=headers)
        status = res.status_code
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Request error:", err)
        return None

    soup = BeautifulSoup(res.text, "lxml")
    table_body = soup.find("tbody")
    if not table_body:
        print("No data found.")
        return None

    result = []

    for row in table_body.find_all("tr"):
        cells = row.find_all("td")

        # Basic fallback
        if len(cells) < 14:
            continue

        # Player name and team
        player_id = cells[0].find("a")["href"].split("/")[-2]
        player_cell = cells[0]
        player_name = player_cell.find("div", class_="text-of")
        player_name = player_name.text.strip() if player_name else "Unknown"
        org = player_cell.find("div", class_="stats-player-country")
        org = org.get_text(strip=True) if org else "Unknown"

        # Agents
        agent_imgs = cells[1].find_all("img")
        agents = [img["src"].split("/")[-1].split(".")[0] for img in agent_imgs]

        # Other stats (grab 11 columns worth)
        stats = [td.text.strip() for td in cells[2:13]]

        result.append({
            "player": player_name,
            "player_id": player_id,
            "org": org,
            "agents": agents,
            "rounds_played": stats[0],
            "rating": stats[1],
            "average_combat_score": stats[2],
            "kill_deaths": stats[3],
            "kast": stats[4],
            "adr": stats[5],
            "kills_per_round": stats[6],
            "assists_per_round": stats[7],
            "first_kills_per_round": stats[8],
            "first_deaths_per_round": stats[9],
            "headshot_percentage": stats[10]
        })

    return {
        "status": status,
        "data": result
    }

if __name__ == "__main__":
    # Example usage
    region = "na"
    timespan = 30  # Days
    player_data = get_all_player_stats(region, timespan)
    if player_data:
        save_to_json(player_data, "vlr_stats.json")
    else:
        print("Failed to retrieve player data.")