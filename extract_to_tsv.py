import json
import argparse

def extract_to_tsv(out_file, json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)


    with open(out_file, 'w') as file:
        file.write("Source\tDate\tTitle\tDescription\tURL\tMovie\tCoding1\tCoding2\n")

        for post in data:
            source_name = post.get('source', {}).get('name', 'N/A')
            published_date = post.get('publishedAt', 'N/A')
            description = post.get('description', 'N/A')
            title = post.get('title', 'N/A').replace("\t", " ")
            url = post.get('url', 'N/A')
            file.write(f"{source_name}\t{published_date}\t{title}\t{description}\t{url}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help="Output TSV file")
    parser.add_argument("json_file", help="Input JSON file with posts")

    args = parser.parse_args()

    extract_to_tsv(args.output, args.json_file)
