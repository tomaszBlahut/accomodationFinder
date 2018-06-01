import json


class RequestParameters:
    def __init__(self, json_data):
        self.__dict__ = json.loads(json_data)
