if __name__ == "__main__":
    with open('combined_res.json', 'r') as file:
        import json
        data = json.loads(file.read())

    metric_exist = data['metric-exist']
    english_exist = data['english-exist']
    total_exist = list(set(metric_exist+english_exist))
    non_exist = data['non-exist']
    all_articles = total_exist+non_exist

    print("---metric---")
    print(f"exist: {len(metric_exist)}")
    print(f"coverage: {len(metric_exist)/len(all_articles)*100}")

    print("---english---")
    print(f"exist: {len(english_exist)}")
    print(f"coverage: {len(english_exist)/len(all_articles)*100}")

    print("---total---")
    print(f"exist: {len(total_exist)}")
    print(f"non-exist: {len(non_exist)}")
    print(f"coverage: {len(total_exist)/len(all_articles)*100}%")
