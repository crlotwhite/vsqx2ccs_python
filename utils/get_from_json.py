import json


def get_from_json(file_path, key):
    with open(file_path) as file:
        json_data = json.loads(file.read())

        try:
            return json_data[key]
        except KeyError:
            return None
