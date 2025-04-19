from get_all_player_stats import get_all_player_stats
from get_player_agent_stats import get_player_agent_stats
import json
import time

def scrape_all_player_stats(region: str = "all", timespan: int = 90) -> dict:
    all_player_agent_stats = []
    data = get_all_player_stats(region=region,timespan=90)
    ids = [id['player_id'] for id in data['data']]
    with open('ids.json', 'w') as f:
        json.dump(ids, f, indent=4)
    for id in ids:
        player_data = get_player_agent_stats(player_id=id, timespan=timespan)
        player_data.pop("status", None)
        player_data["data"].pop("url", None)
        all_player_agent_stats.append(player_data["data"])
        time.sleep(.25)
        
    # Save the data to a file or database as needed
    with open('all_player_agent_stats.json', 'w') as f:
        json.dump(all_player_agent_stats, f, indent=4)
    return all_player_agent_stats

        

scrape_all_player_stats(region="all", timespan=90)