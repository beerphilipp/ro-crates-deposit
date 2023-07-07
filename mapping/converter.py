import sys
import json

import processing_functions as pf
import condition_functions as cf

def main():
    """
        For test purposes only.
    """
    if (len(sys.argv) != 2):
        print("Usage: python converter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = input_file.replace(".rc.json", ".dc.json")
    f = open(input_file)
    rc = json.load(f)

    output = convert(rc)

    with open(output_file, 'w') as outfile:
        json.dump(output, outfile, indent=4)

    return


def convert(rc):
    mapping_file = open("mapping/mapping.json")
    m = json.load(mapping_file)

    dc = setup_dc()
    print(dc)

    root_rules = m.get("$root")
    
    for mapping_class in root_rules:
        print()
        
        # Ignore mappings that are marked as ignored
        if ("_ignore" in root_rules.get(mapping_class).keys()):
            print(f"|x Ignoring {mapping_class}")
            continue
        
        print(f"|- Applying rule collection {mapping_class}")
        
        root_mappings = root_rules.get(mapping_class)
        
        # TODO: implement ifNonePresent behaviour
        mappings = root_mappings.get("mappings")

        is_any_present = False

        for mapping_key in mappings:
            # TODO: implement proper array mapping behaviour
            print(f"\t|- Applying mapping {mapping_key}")
                
            mapping = mappings.get(mapping_key)

            if ("_ignore" in mapping.keys()):
                continue
            
            from_mapping_value = mapping.get("from")
            to_mapping_value = mapping.get("to")
            value_mapping_value = mapping.get("value")
            processing_mapping_value = mapping.get("processing")
            only_if_value = mapping.get("onlyIf")

            # The following steps are performed:
            # 1. Get the value from the RO-Crate (from)
            # 2. Check if the rule should be applied (onlyIf)
            # 3. Process the value (processing)
            # 4. Put the value into the correct format (value)
            # 5. Add the value to the DataCite object (to)

            from_value = get_rc(rc, from_mapping_value)
            
            if (from_value == None):
                continue

            if (only_if_value != None):
                print(f"\t\t|- Checking condition {only_if_value}")
                if (not check_condition(only_if_value, from_value)):
                    continue

            if processing_mapping_value:
                from_value = process(processing_mapping_value, from_value)
            
            if value_mapping_value:
                from_value = transform_to_target_format(value_mapping_value, from_value)
            
            if dc != None:
                dc = set_dc(dc, to_mapping_value, from_value)
                is_any_present = True
        
        if (not is_any_present):
            none_present_value = root_mappings.get("ifNonePresent")
            if (none_present_value != None):
                print(f"\t|- Applying ifNonePresent rule {none_present_value}")
                for none_present_key in none_present_value:
                    none_present_mapping_value = none_present_value.get(none_present_key)
                    dc = set_dc(dc, none_present_key, none_present_mapping_value)

    return dc


def rc_get_rde(rc):
    """
        Retrieves the Root Date Entity from the given RO-Crate.

        :param rc: The RO-Crate to retrieve the RDE from.
        :return: The Root Data Entity of the given RO-Crate.
    """

    # Following the RO-Crate specification (https://www.researchobject.org/ro-crate/1.1/root-data-entity.html), 
    # use the following algorithm to find the RDE:
    #
    # For each entity in @graph array
    #   if the conformsTo property is a URI that starts with https://w3id.org/ro/crate/
    #       from this entity's about object keep the @id URI as variable root
    # For each entity in @graph array
    #   if the entity has an @id URI that matches the root return it
    
    root = None
    graph = rc.get("@graph")
    for entity in graph:
        conformsTo = entity.get("conformsTo")
        if (conformsTo and conformsTo.get("@id") and conformsTo.get("@id").startswith("https://w3id.org/ro/crate/")):
            root = entity.get("about").get("@id")
    
    for entity in graph:
        if (entity.get("@id") == root):
            return entity


def transform_to_target_format(format, value):
    """
        Transforms the given value to the given format.
        The format parameter is a string, which can contain the following special values:
            - @@this: The value of the key itself
        
        :param format: The format to apply to the value.
        :param value: The value to format.
        :return: The formatted value.
    """
    if (format != None):
        if ("@@this." in format):
            raise NotImplemented(f"Indexing of @@-prefixed value formatting not yet implemented.")
        
        if (value):
            print(f"\t\t|- Formatting value according to {format}.")
            value = format_value(format, value)
        print(f"\t\t|- Formatted value is {value}")
    return value


def get_rc(rc, from_key):
    """
        Retrieves the value of the given key from the given RO-Crate.
        A key consists of multiple subkeys, separated by a dot (.).
        If a subkey starts with a $, then it is a reference to another key.

        :param rc: The RO-Crate to retrieve the value from.
        :param from_key: The key to retrieve the value from.
        :return: The value of the given key in the given RO-Crate.
    """
    result = None

    if from_key:
        print(f"\t\t|- Retrieving value {from_key} from RO-Crate.")
        keys = from_key.split(".")
        temp = rc_get_rde(rc)
        print(temp)

        for key in keys:
            if (key.startswith("$")):
                # we need to dereference the key
                temp = get_rc_ref(rc, temp, key)
                if (temp == None):
                    return None
            
            elif (key not in temp.keys()):
                # The key could not be found in the RO-Crate
                return None
            
            else:
                temp = temp.get(key)
        
        result = temp

    print(f"\t\t|- Value for key {from_key} is {result}")

    if (result and isinstance(result, dict)):
        # If the value is a JSON object, then we ignore the rule (since another rule must be implemented on how to handle it)
        return None
    
    return result

def get_rc_ref(rc, parent, from_key):
    """
        Retrieves the entity referenced by the given $-prefixed key from the given RO-Crate.
        
        Example: Calling get_rc_ref(rc, parent, "$affiliation") on the following RO-Crate

        rc: {
            ...
            {
                "@id": "https://orcid.org/0000-0002-8367-6908",
                "@type": "Person",
                "name": "J. Xuan"
                "affiliation": {"@id": "https:/abc"}
            }
            {
                "@id": "https:/abc",
                "@type": "Organization",
                "name": "ABC University"
            }
        }

        parent: {
                "@id": "https://orcid.org/0000-0002-8367-6908",
                "@type": "Person",
                "name": "J. Xuan"
                "affiliation": {"@id": "https:/abc"}
            }

        returns {
                "@id": "https:/abc",
                "@type": "Organization",
                "name": "ABC University"
            }
    """
    print(f"\t\t|- Retrieving referenced entity {from_key} from RO-Crate.")
    if (from_key and not from_key.startswith("$")):
        raise Exception(f"$-prefixed key expected, but {from_key} found.")
    
    id_val = parent.get(from_key[1:])
    if (isinstance(id_val, dict)):
        id = id_val.get("@id")
        print(f"\t\t\t|- Id is {id}")
    else:
        return None
    
    for entity in rc.get("@graph"):
        if (entity.get("@id") == id):
            print(f"\t\t\t|- Found entity {entity}")
            return entity
    
    return None
 

def get_rc_ref_root(rc, from_key):
    """
        Retrieves the entity referenced by the given $-prefixed key from the given RO-Crate.

        :param rc: The RO-Crate to retrieve the referenced entity from.
        :param from_key: The $-prefixed key to retrieve the referenced entity from.
        :return: The referenced entity of the given RO-Crate.
    """
    print(f"\t\t|- Retrieving referenced entity {from_key} from RO-Crate.")
    if (from_key and not from_key.startswith("$")):
        raise Exception(f"$-prefixed key expected, but {from_key} found.")
    
    keys = from_key.split(".")
    root = rc_get_rde(rc)
    if (root.get(keys[0][1:]) == None):
        print(f"\t\t|- Key {keys[0]} not found in RO-Crate.")
        return None
    target_entity_id = root.get(keys[0][1:]).get("@id")
    target_entity = None

    for entity in rc.get("@graph"):
        if (entity.get("@id") == target_entity_id):
            target_entity = entity
            break
    return target_entity

def format_value(format, value):
    """
        Formats the given value according to the given format.
        The format can be a string or a dictionary.
        If the format is a string, the value is inserted at the position of @@this.
        If the format is a dictionary, the value is inserted at the position of @@this in each value of the dictionary.

        For example, if the format is {"a": "@@this", "b": "c"}, and the value is "d", the result is {"a": "d", "b": "c"}.

        :param format: The format to use.
        :param value: The value to insert.
        :return: The formatted value.
    """
    if isinstance(format, str):
        return format.replace("@@this", value)
    elif isinstance(format, dict):
        #format = {}
        for key, v in format.items():
            if isinstance(v, str):
                format[key] = v.replace("@@this", value)
            else:
                format[key] = v
        return format
    else:
        raise TypeError(f"Format must be a string or a dictionary, but is {type(format)}.")

def set_dc(dictionary, key, value=None, add_to=-1):
    keys = key.split(".")
    current_dict = dictionary
    for key_part in keys:
        print(key_part)
        
        if key_part.endswith("[]") and not key_part[:-2] in current_dict:
            current_dict[key_part[:-2]] = [{}]
            last_val = current_dict[key_part[:-2]]
            current_dict = current_dict[key_part[:-2]][0]
        
        elif key_part.endswith("[]") and key_part[:-2] in current_dict:
            last_val = current_dict[key_part[:-2]]
            current_dict = current_dict[key_part[:-2]][0]
        
        elif not key_part in current_dict and not key_part.endswith("[]"):
            last_val = current_dict
            current_dict[key_part] = {}
            current_dict = current_dict[key_part]

        else:
            last_val = current_dict
            current_dict = current_dict[key_part]
            
    last_key = keys[-1]
    if last_key.endswith("[]"):
        last_val[0] = value
    else:
        last_val[last_key] = value
    return dictionary


def check_condition(condition_rule, value):
    """
        Checks if a value matches a condition rule.
        The condition rule is a string that starts with ? and is followed by the name of the function to apply.
        The function must be defined in condition_functions.py.

        :param condition_rule: The condition rule to apply.
        :param value: The value to check.
        :return: True if the value matches the condition, False otherwise.
    """
    if (not condition_rule.startswith("?")):
        raise Exception(f"Condition rule {condition_rule} must start with ?")
    try:
        function = getattr(cf, condition_rule[1:])
    except AttributeError:
        raise NotImplementedError(f"Function {condition_rule} not implemented.")
    return function(value)


def process(process_rule, value):
    """
        Processes a value according to a processing rule.
        The processing rule is a string that starts with $ and is followed by the name of the function to apply.
        The function must be defined in processing_functions.py.

        :param process_rule: The processing rule to apply.
        :param value: The value to process.
        :return: The processed value.
    """
    if (not process_rule.startswith("$")):
        raise Exception(f"Processing rule {process_rule} must start with $")
    try:
        function = getattr(pf, process_rule[1:])
    except AttributeError:
        raise NotImplementedError(f"Function {process_rule} not implemented.")
    return function(value)


def setup_dc():
    # https://inveniordm.docs.cern.ch/reference/metadata/#metadata
    dc = {
        #"id": { }, # The value of the internal record identifier.
        #"pid": { }, # Object level information about the identifier needed for operational reasons.
        #"parent": { # parent.pid: the value of the concept record identifier.
        #    "id": { },
        #    "access": {
        #        "owned_by": [
        #            { "user": 1 } # id of user
        #         ] # array of owners
        #    }
        #}, 
        #"pids": { },
        "access": { 
            "record": "public", # public or restricted; 1
            "files": "public", # public or restricted; 1
            "embargo": { # 0-1
                "active": False, # boolean; 1
                #"until": "2020-01-01", # ISO date string; 0-1
                #"reason": "" #0-1 
            }
        },
        "metadata": { },
        "files": { 
            "enabled": True # figure out if we have to change this
        },
        #"tombstone": { }
        }
    return dc



if __name__ == "__main__":
    main()