import json
import asyncio
from aiohttp import ClientSession, ClientConnectorError


exist_articles = []
non_existent_articles = []
strange_articles = []


async def fetch_html(article: str, session: ClientSession, **kwargs) -> tuple:
    url = f"https://catalog.belden.com/techdatam/{article}.pdf"
    try:
        resp = await session.request(method="GET", url=url, **kwargs)
    except ClientConnectorError:
        return (400, article)
    if len(resp.history) > 0:
        return (404, article)
    return (resp.status, article)


async def make_requests(articles_set: set, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        for article in articles_set:
            tasks.append(
                fetch_html(article=article, session=session, **kwargs)
            )
        results = await asyncio.gather(*tasks)

    for result in results:
        # print(f'{result[0]} - {str(result[1])}')
        if result[0] == 200:
            exist_articles.append(result[1])
        elif result[0] == 404:
            non_existent_articles.append(result[1])
        else:
            strange_articles.append(result[1])

if __name__ == "__main__":
    import pathlib
    import sys
    import time

    start_time = time.time()

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent

    with open("data.json", "r") as file:
        data = json.loads(file.read())
        articles_set = set(data["article_list"][0: 1000])

    asyncio.get_event_loop().run_until_complete(make_requests(
        articles_set=articles_set))

    with open("output.json", "w") as file:
        file.write(json.dumps({
            "exist": exist_articles,
            "non-exist": non_existent_articles,
            "strange": strange_articles
        }))

    print(f"End time: {time.time()- start_time}")
