import requests
from bs4 import BeautifulSoup


def vlr_stats(region: str, timespan: int):
    
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
    print(table_body)
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
        player_cell = cells[0]
        player_name = player_cell.find("a", class_="text-of").text.strip()
        org = player_cell.find("div", class_="ge-text-light").text.strip() if player_cell.find("div", class_="ge-text-light") else "N/A"

        # Agents
        agent_imgs = cells[1].find_all("img")
        agents = [img["src"].split("/")[-1].split(".")[0] for img in agent_imgs]

        # Other stats (grab 11 columns worth)
        stats = [td.text.strip() for td in cells[2:13]]

        result.append({
            "player": player_name,
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


# Example usage:
def main():
    data = vlr_stats("all", 30)