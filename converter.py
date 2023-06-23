import sys
import json

def main():
    
    if (len(sys.argv) != 2):
        print("Usage: python converter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    #output_file = sys.argv[2]

    # Opening JSON file
    f = open(input_file)

    # returns JSON object as a dictionary
    data = json.load(f)

    # print one element of the data
    print(data['@graph'][0]["@type"])

    print(len(data['@graph']))

#    for i in range(len(data['@graph'])):

#        print(i, " -------- ", data['@graph'][i])

    print("Hierarch of json with datatypes: ")

    print(type(data['@context']), 'name: @context: ', 'value:', data['@context'])
    print(type(data['@graph']))
    print(type(data['@graph'][0]))
    print(type(data['@graph'][0]["@type"]))

    # Closing file
    f.close()
if __name__ == "__main__":
    main()