def common_keys_comparsion(dict1, dict2):
    common_keys = dict1.keys() & dict2.keys()
    for key in common_keys:
        if dict1[key] != dict2[key]:
            return False
    return True