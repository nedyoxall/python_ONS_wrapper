import yaml
import requests
import requests_cache
import json
import pickle
import os.path
import pandas as pd
import itertools

from helper_funcs import pretty_print_json

def get_dataset(reference, context, geog, cache=False):
    """

    :param reference:
    :param context:
    :param geog:
    :param cache:
    :return:
    """

    with open('../config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    obs_count = get_dataset_observation_count(reference, context, geog, config['apikey'])
    if obs_count > 100000:
        print 'Observation Count: ' + str(obs_count) + ' (max for json-stat is 100,000).'
        raise NotImplementedError('Dataset too large.')

    url = 'http://data.ons.gov.uk/ons/api/data/dataset/' + reference + '.json?context=' + context + \
          '&geog=' + geog + '&apikey=' + config['apikey'] + '&jsontype=json-stat'

    print url

    if cache:
        requests_cache.install_cache()

    request_json = requests.get(url)
    response = json.loads(request_json.text)
    try:
        data = response[reference]
    except KeyError:
        print response['dataPackage']['errorMessage']
        raise


    ########################## General info about the dataset
    data_source = data['source']
    data_last_updated = data['updated']
    data_label = data['label']

    ########################## dimensions

    # Different dimensions within the dataset
    dimensions = data['dimension']

    dimension_roles = dimensions['role']

    dimension_sizes = dimensions['size']
    number_of_dims = sum(x > 1 for x in dimension_sizes)

    dimension_ids = dimensions['id']

    if number_of_dims == 3:
        z_dim_id, y_dim_id, x_dim_id = dimension_ids[0], dimension_ids[1], dimension_ids[2]
    elif number_of_dims == 2:
        y_dim_id, x_dim_id = dimension_ids[0], dimension_ids[1]
    else:
        raise NotImplementedError("Neither 2 or 3 dimensions.")

    if number_of_dims == 3:
        z_dim_size, y_dim_size, x_dim_size = dimension_sizes[0], dimension_sizes[1], dimension_sizes[2]
    elif number_of_dims == 2:
        y_dim_size, x_dim_size = dimension_sizes[0], dimension_sizes[1]


    if number_of_dims == 3:
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

    if number_of_dims == 3:
        dfs = []
        for k in range(z_dim_size):
            table = []
            for j in range(y_dim_size):
                record = []
                for i in range(x_dim_size):
                    record.append(values_cube[str(y_dim_size*x_dim_size*k + x_dim_size*j + i)])
                table.append(record)
            df = pd.DataFrame.from_records(table, index=y_dim_labels, columns=x_dim_labels)
            dfs.append(df)

        return pd.concat({label: df for (label, df) in zip(z_dim_labels, dfs)})

    elif number_of_dims == 2:
        table = []
        for j in range(y_dim_size):
            record = []
            for i in range(x_dim_size):
                record.append(values_cube[str(x_dim_size * j + i)])
            table.append(record)
        df = pd.DataFrame.from_records(table, index=y_dim_labels, columns=x_dim_labels)

        return df

def get_dataset_observation_count(reference, context, geog, apikey):
    """

    :param reference:
    :param context:
    :param geog:
    :param apikey:
    :return:
    """
    url = 'http://data.ons.gov.uk/ons/api/data/datasetdetails/' + reference + \
          '.json?context=' + context + '&geog=' + geog + '&apikey=' + apikey

    request_json = requests.get(url)
    response = json.loads(request_json.text)
    return response['ons']['datasetDetail']['obsCount']


df = get_dataset('DC1202EW', 'Census', '2011HTWARDH', cache = True)
print df






