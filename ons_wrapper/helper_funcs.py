import json


def pretty_print_json(json_obj):
    print json.dumps(json_obj, indent=2)