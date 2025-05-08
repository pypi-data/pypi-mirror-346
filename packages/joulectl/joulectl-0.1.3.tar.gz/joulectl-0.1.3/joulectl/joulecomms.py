import requests
import json

def callServer(method: str, url: str, host: str, headers: dict, params: dict):
    try:
        response = requests.request(method=method, url=url, headers=headers, params=params)
    except requests.ConnectionError as e:
        print("Error connecting to Joule server: {}".format(host))
        exit(1)
    return response


def postData(url: str, filename: str, params: dict, host: str, headers: dict):
    with open(filename) as json_data:
        data = json.load(json_data)
        try:
            response = requests.post(url, headers=headers, json=data, params=params)
        except requests.ConnectionError as e:
            print("Error connecting to Joule server: {}".format(host))
            exit(1)
    return response