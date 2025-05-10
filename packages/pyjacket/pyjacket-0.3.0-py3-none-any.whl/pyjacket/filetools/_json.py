import json

def read_json(filepath: str, **kwargs) -> dict:
    with open(filepath, 'r') as f:
        data = json.load(f, **kwargs)
    return data

def write_json(filepath: str, data: dict, **kwargs):
    with open(filepath, 'w') as f:
        json.dump(data, f, **kwargs)