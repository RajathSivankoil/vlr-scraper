import json
from get_all_player_stats import get_player_agent_stats

# Manually saving to JSON file for testing purposes
def save_to_json(data: dict, filename: str) -> None:
    if data is None:
        return None
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def player_stats_to_json(player_id: int, timespan: int = 30) -> None:
    player_data = get_player_agent_stats(player_id, timespan)
    save_to_json(player_data, 'current_player_stats.json')