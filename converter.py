import sys
import json

def main():
    
    if (len(sys.argv) != 2):
        print("Usage: python converter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    #output_file = sys.argv[2]

    #-----------------------
    mapping = open("mapping.json")
    m = json.load(mapping)

    print(m)

    # -----------------------


    # Opening JSON file
    f = open(input_file)

    # returns JSON object as a dictionary
    data = json.load(f)
    """
    # print one element of the data
    print(data['@graph'][0]["@type"])

    print(len(data['@graph']))

#    for i in range(len(data['@graph'])):

#        print(i, " -------- ", data['@graph'][i])

    print("Hierarch of json with datatypes: ")

    print(type(data['@context']), 'name: @context: ', 'value:', data['@context'])
    print("")
    print(type(data['@graph']), 'name: @graph', 'value:', data['@graph'])
    print("AAAAA")
    print(type(data['@graph'][0]), 'sub-dictionary:', data['@graph'][0])
    print("")
    print(type(data['@graph'][0]["@type"]), "element:", data['@graph'][0]["@type"])
    print(type(data['@graph'][1]), 'sub-dictionary:', data['@graph'][1])
    print("")
    print(type(data['@graph'][1]["@type"]), "element:", data['@graph'][1]["@type"])


    # Closing file
    f.close()

    # Merge input json file with mapping
    # and create output file

    # data should be the converted file
    json_object = json.dumps(data, indent=2)

    with open("output.json", 'w') as out:
        out.write(json_object)



    """
if __name__ == "__main__":
    main()