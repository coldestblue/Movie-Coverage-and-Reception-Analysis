import json
import argparse

def extract_to_tsv(out_file, json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)


    with open(out_file, 'w') as file:
        file.write("Name\ttitle\tcoding\n")

        for post in data:
            source_name = post.get('source', {}).get('name', 'N/A')
            author = post.get('author', 'N/A')
            title = post.get('title', 'N/A').replace("\t", " ")
            file.write(f"{source_name}\t{author}\t{title}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help="Output TSV file")
    parser.add_argument("json_file", help="Input JSON file with posts")

    args = parser.parse_args()

    extract_to_tsv(args.output, args.json_file)
