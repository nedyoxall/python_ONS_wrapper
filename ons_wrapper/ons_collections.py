import yaml


baseurl = 'http://data.ons.gov.uk/ons/api/data/'

with open('../config.yaml', 'r') as f:
    config = yaml.safe_load(f)

add = baseurl + 'collections.json?context=Census&apikey=' + config['apikey']

print add

import requests
