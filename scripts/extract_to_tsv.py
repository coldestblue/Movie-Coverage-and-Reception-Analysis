import json
import argparse
import html

def extract_to_tsv(out_file, json_file):
    def sanitize(text):
        if not text: 
            return "N/A"
        text = text.replace("\n", " ").replace("\t", " ") 
        text = html.unescape(text)
        return text

    with open(json_file, 'r') as file:
        data = json.load(file)

    with open(out_file, 'w') as file:
        
        file.write("Source\tDate\tTitle\tDescription\tURL\tMovie\tCoding1\tCoding2\n")

        for post in data:
            source_name = sanitize(post.get('source', {}).get('name', 'N/A'))
            published_date = sanitize(post.get('publishedAt', 'N/A'))
            description = sanitize(post.get('description', 'N/A'))
            title = sanitize(post.get('title', 'N/A'))
            url = sanitize(post.get('url', 'N/A'))

            if not source_name.strip() or source_name == 'N/A':
                continue
            if not published_date.strip() or published_date == 'N/A':
                continue
            if not title.strip() or title == 'N/A':
                continue
            if not url.strip() or url == 'N/A':
                continue

            file.write(f"{source_name}\t{published_date}\t{title}\t{description}\t{url}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help="Output TSV file")
    parser.add_argument("json_file", help="Input JSON file with posts")

    args = parser.parse_args()

    extract_to_tsv(args.output, args.json_file)
    print("done")