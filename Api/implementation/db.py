import json
import dataset

with open('config/config.json') as json_data:
    config = json.load(json_data)

db_config = config["database"]


def get_database_connection_params():
    database_url = 'postgresql://%(username)s:%(password)s@%(host)s/%(db_name)s' % db_config
    schema = db_config['schema']
    return database_url, schema
