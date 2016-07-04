import yaml
import requests
import json
import os.path
import pandas as pd
import itertools


def get_collections_details(context):
    """
    #TODO - useful docstring!!!
    :return:
    """
    if context not in ['Census', 'Socio-Economic','Social','Economic']:
        raise ValueError('The input context must be one of Census, Socio-Economic, Social or Economic.')


    print 'Checking to see if < 1 week old collections data already exists...'

    if os.path.isfile('../data/' + context.lower() + '_collections_df.pkl'):  # TODO add in date functionality
        print 'Data found.'
        collections_df = pd.read_pickle('../data/' + context.lower() + '_collections_df.pkl')

    else:
        print 'Data not found. Requesting from ONS API...'
        base_url = 'http://data.ons.gov.uk/ons/api/data/'
        with open('../config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        url = base_url + 'collections.json?context=' + context + '&apikey=' + config['apikey']

        request_json = requests.get(url)
        collections_json = json.loads(request_json.text)

        print 'Request completed... Saving as DataFrame.'

        collections_count = collections_json['ons']['collectionList']['collectionCount']

        coll_ids, coll_descs, coll_times, coll_geotypes, coll_names = [],[],[],[],[]
        for i in range(collections_count):
            this_coll = collections_json['ons']['collectionList']['collection'][i]

            this_id = [this_coll['id']]
            this_desc = [this_coll['description']]
            this_name = [this_coll['names']['name'][0]['$']]


            this_geo = this_coll['geographicalHierarchies']['geographicalHierarchy']
            if isinstance(this_geo, list):
                length = len(this_geo)
                this_time, this_geotype = [],[]
                for j in range(length):
                    this_time.append(this_geo[j]['time'])
                    this_geotype.append(this_geo[j]['geographicalType'][0]['$'])
                this_id *= length
                this_desc *= length
                this_name *= length


            elif isinstance(this_geo, dict):
                this_time = [this_geo['time']]
                this_geotype = [this_geo['geographicalType'][0]['$']]

            coll_ids.append(this_id)
            coll_descs.append(this_desc)
            coll_times.append(this_time)
            coll_geotypes.append(this_geotype)
            coll_names.append(this_name)

        collections_df = pd.DataFrame({'ID' : list(itertools.chain(*coll_ids)),
                                       'Description' : list(itertools.chain(*coll_descs)),
                                       'Time' : list(itertools.chain(*coll_times)),
                                       'Geography' : list(itertools.chain(*coll_geotypes)),
                                       'Name' : list(itertools.chain(*coll_names))})

        collections_df.to_pickle('../data/' + context.lower() + '_collections_df.pkl')

    return collections_df








