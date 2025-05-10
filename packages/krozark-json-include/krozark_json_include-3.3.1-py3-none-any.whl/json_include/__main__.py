from .json_include import build_str
import argparse

def main():
    parser = argparse.ArgumentParser(prog="json-build")
    parser.add_argument("filepath", help="JSON file to build")
    args = parser.parse_args()

    data = build_str(args.filepath)
    print(data)

if __name__ == "__main__":
    main()