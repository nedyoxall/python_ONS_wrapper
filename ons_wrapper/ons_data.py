import yaml
import requests
import json
import pickle
import os.path
import pandas as pd
import itertools



def get_dataset(reference, context, geog):
    base_url = 'http://data.ons.gov.uk/ons/api/data/'


    with open('../config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    url = base_url + 'dataset/' + reference + '.json?context=' + context + \
          '&geog=' + geog + '&apikey=' + config['apikey'] + '&jsontype=json-stat'

    request_json = requests.get(url)
    data = json.loads(request_json.text)[reference]

    # General info about the dataset
    data_source = data['source']
    data_last_updated = data['updated']
    data_label = data['label']

    # Different dimensions within the dataset
    dimensions = data['dimension']

    dimension_ids = dimensions['id']
    dimension_sizes = dimensions['size']
    dimension_roles = dimensions['role']

    # Now need to deal with all the different dimensions...
    print dimension_ids


get_dataset('AP1101EW', 'Census', '2011WARDH')


