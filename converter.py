import sys

def main():
    
    if (len(sys.argv) != 3):
        print("Usage: python converter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

if __name__ == "__main__":
    main()