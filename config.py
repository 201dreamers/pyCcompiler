import json


CONFIG_FILE = 'settings.json'

with open(CONFIG_FILE, 'r') as conf_file:
    config_data = json.load(conf_file)

PATH_TO_SOURCE_FILE = config_data['path_to_source_file']
PATH_TO_OUTPUT_FILE = config_data['path_to_output_file']