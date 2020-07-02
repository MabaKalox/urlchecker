import pandas
import json

if __name__ == "__main__":
    def parse_to_json(filePath):
        table = pandas.read_excel(filePath, sheet_name="blad 1")
        table_json_Str = table.to_json(orient='records')
        table_json = json.loads(table_json_Str)
        article_list = []
        for row in table_json:
            key = next(iter(row.keys()))
            article = str(row[key])
            article_list.append(article)
        article_list = article_list[6: len(article_list)]
        return {"article_list": article_list}

    data = parse_to_json("data.xlsx")
    with open("data.json", "w") as file:
        file.write(json.dumps(data, indent=4))
