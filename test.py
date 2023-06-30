def access_nested_dict(dictionary, key, value=None, add_to=-1):
    keys = key.split(".")
    current_dict = dictionary
    in_array = False
    for key_part in keys[:-1]:
        if key_part.endswith("[]"):
            in_array = True
            array_key = key_part.rstrip("[]")
            if array_key not in current_dict:
                current_dict[array_key] = []
            current_dict = current_dict[array_key]
        else:
            if key_part not in current_dict:
                current_dict[key_part] = {}
            current_dict = current_dict[key_part]
    
    print(dictionary)
    
    last_key = keys[-1]
    if last_key.endswith("[]"):
        array_key = last_key[:-2]
        if len(current_dict) == 0:
            current_dict[array_key] = []
            add_to = 0
        print(add_to)
        if (add_to != -1):
            current_dict[add_to][array_key] = value
        else:
            current_dict.append({array_key: value})
        return dictionary
    
    elif last_key.endswith("[]") and in_array:
        raise Exception("Nested array not supported.")
    
    elif not last_key.endswith("[]") and in_array:
        if len(current_dict) == 0:
            current_dict.append({})
            add_to = 0
        if (add_to != -1):
            current_dict[add_to][last_key] = value
        else:
            current_dict.append({last_key: value})
        return dictionary
    
    else:
        if last_key not in current_dict or add_to != -1:
            current_dict[last_key] = value

    return dictionary

dict = {'a': {'b': {'c': [{'d': "E"}]}}}

print(access_nested_dict(dict, "a.b.c[].e", value="ABC", add_to=0))