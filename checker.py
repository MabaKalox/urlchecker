import concurrent.futures
import requests
import time
import json

if __name__ == "__main__":

    out = []
    CONNECTIONS = 50
    TIMEOUT = 50
    exist_articles = []
    non_existent_articles = []
    strange_articles = []

    with open("data.json", "r") as file:
        data = json.loads(file.read())
        articles_list = data["article_list"]

    def load_url(article, timeout):
        url2 = f"https://catalog.belden.com/techdata/EN/{article}_techdata.pdf"
        url = f"https://catalog.belden.com/techdatam/{article}.pdf"
        ans = requests.get(url, timeout=timeout)
        if len(ans.history) == 0 and ans.status_code == 200:
            return (200, article)
        else:
            return (404, article)

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=CONNECTIONS) as executor:
        future_to_url = []
        for article in articles_list:
            future_to_url.append(executor.submit(load_url, article, TIMEOUT))
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = (str(exc), None)
            finally:
                if data[0] == 200:
                    exist_articles.append(data[1])
                else:
                    non_existent_articles.append(data[1])

        time2 = time.time()

    print(f'Took {time2-time1:.2f} s')
    with open("output.json", "w") as file:
        file.write(json.dumps({
            "exist": exist_articles,
            "non-exist": non_existent_articles,
        }))
