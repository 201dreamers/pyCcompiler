import json

from loguru import logger


logger.add('debug.log', level='ERROR')

CONFIG_FILE = 'settings-lab.json'

with open(CONFIG_FILE, 'r') as conf_file:
    config_data = json.load(conf_file)

PATH_TO_SOURCE_FILE = config_data['path_to_source_file']
PATH_TO_OUTPUT_FILE = config_data['path_to_output_file']
