import concurrent.futures
import requests
import time
import json
from typing import List


patern_placeholder = '{placeholder}'


def check_article_list(article_list: List[str], pattern: str,
                       CONNECTIONS: int = 60, TIMEOUT: int = 50):
    exist_articles = []
    non_existent_articles = []
    pdf_bytecode_list = []

    def load_url(article, timeout):
        url = pattern.replace(patern_placeholder, article)
        ans = requests.get(url, timeout=timeout)
        if ans.content[1:4] == b'PDF':
            return (200, article, ans.content)
        else:
            return (404, article, None)

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=CONNECTIONS) as executor:
        future_to_url = []
        for article in articles_list:
            future_to_url.append(executor.submit(load_url, article, TIMEOUT))
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            if data[0] == 200:
                pdf_bytecode_list.append(data[2])
                exist_articles.append(data[1])
            else:
                non_existent_articles.append(data[1])

        time2 = time.time()

    print(f'Took {time2-time1:.2f} s')
    return {
        "exist": exist_articles,
        "non-exist": non_existent_articles,
        "pdf_bytecode_list": pdf_bytecode_list,
    }


if __name__ == "__main__":
    metric_dock_url_pattern = f"https://catalog.belden.com/techdatam/{patern_placeholder}.pdf"  # noqa: E501
    english_dock_url_pattern = f"https://catalog.belden.com/techdata/EN/{patern_placeholder}_techdata.pdf"  # noqa: E501

    with open("data.json", "r") as file:
        data = json.loads(file.read())
        articles_list = data['article_list']

        metric_res = check_article_list(articles_list,
                                        pattern=metric_dock_url_pattern)
        english_res = check_article_list(articles_list,
                                         pattern=english_dock_url_pattern)

        # write existance info
        non_exist = set(metric_res['non-exist'])
        non_exist.intersection_update(set(english_res['non-exist']))

        output_data = {
            "english-exist": None,
            "metric-exist": None,
            "non-exist": None
        }
        output_data['metric-exist'] = metric_res['exist']
        output_data['english-exist'] = english_res['exist']
        output_data['non-exist'] = list(non_exist)

        with open("combined_res.json", "w") as file:
            file.write(json.dumps(output_data, indent=4))

        # write to pdfs
        pdf_metric_data = []
        for article in metric_res['exist']:
            pdf_metric_data.append({"article": article})
        for i, bytecode in enumerate(metric_res['pdf_bytecode_list']):
            pdf_metric_data[i]["pdf"] = bytecode

        for data in pdf_metric_data:
            article = data["article"]
            pdf = data["pdf"]
            with open(f"docs/metric/{article}.pdf", "bw") as file:
                file.write(pdf)
