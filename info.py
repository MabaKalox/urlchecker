if __name__ == "__main__":
    with open('output.json', 'r') as file:
        import json
        data = json.loads(file.read())

    exist_articles = data["exist"]
    nonexist_articles = data["non-exist"]

    total = len(exist_articles)+len(nonexist_articles)

    print(f"total: {total}")
    print(f"exist: {len(exist_articles)}")
    print(f"non-exist: {len(nonexist_articles)}")
    print(f"exist: {len(exist_articles)/total*100}%")
