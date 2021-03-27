import json


def save_last_id(state, last_id):
    with open('tweetcollector/last_id.json', 'r') as file:
        json_data = json.load(file)
        for item in json_data:
            if item['state'] in [state]:
                item['last_id'] = last_id
    with open('tweetcollector/last_id.json', 'w') as file:
        json.dump(json_data, file, indent=2)

def get_last_id(state):
    with open('tweetcollector/last_id.json', 'r') as file:
        json_data = json.load(file)
        for item in json_data:
            if item['state'] in [state]:
                return item['last_id']