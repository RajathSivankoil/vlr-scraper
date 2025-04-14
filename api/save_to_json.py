import json

# Manually saving to JSON file for testing purposes
def save_to_json(data: dict, filename: str) -> None:
    if data is None:
        return None
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)