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

    ########################## General info about the dataset
    data_source = data['source']
    data_last_updated = data['updated']
    data_label = data['label']

    ########################## dimensions

    # Different dimensions within the dataset
    dimensions = data['dimension']

    dimension_roles = dimensions['role']

    dimension_ids = dimensions['id']
    z_dim_id, y_dim_id, x_dim_id = dimension_ids[0], dimension_ids[1], dimension_ids[2]

    dimension_sizes = dimensions['size']
    z_dim_size, y_dim_size, x_dim_size = dimension_sizes[0], dimension_sizes[1], dimension_sizes[2]

    z_dim_codes_reverse_dict = dimensions[z_dim_id]['category']['index']
    z_dim_labels_dict = dimensions[z_dim_id]['category']['label']
    z_dim_codes_dict =  {v:k for k,v in z_dim_codes_reverse_dict.iteritems()}
    z_dim_labels = [z_dim_labels_dict[x] for x in z_dim_codes_dict.values()]

    y_dim_codes_reverse_dict = dimensions[y_dim_id]['category']['index']
    y_dim_labels_dict = dimensions[y_dim_id]['category']['label']
    y_dim_codes_dict = {v: k for k, v in y_dim_codes_reverse_dict.items()}
    y_dim_labels = [y_dim_labels_dict[x] for x in y_dim_codes_dict.values()]

    x_dim_codes_reverse_dict = dimensions[x_dim_id]['category']['index']
    x_dim_labels_dict = dimensions[x_dim_id]['category']['label']
    x_dim_codes_dict = {v: k for k, v in x_dim_codes_reverse_dict.iteritems()}
    x_dim_labels = [x_dim_labels_dict[x] for x in x_dim_codes_dict.values()]

    ######################## values

    values_cube = data['value']

    dfs = []
    for k in range(z_dim_size):
        table = []
        for j in range(y_dim_size):
            record = []
            for i in range(x_dim_size):
                record.append(values_cube[str(y_dim_size*k + x_dim_size*j + i)])
            table.append(record)
        df = pd.DataFrame.from_records(table, index=y_dim_labels, columns=x_dim_labels)
        dfs.append(df)

    print dfs[0]



get_dataset('AP1101EW', 'Census', '2011WARDH')


