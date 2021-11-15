from typing import Tuple
import aiohttp
import asyncio

baseUrl = "https://hacker-news.firebaseio.com/v0"


async def get_latest_stories() -> Tuple:
    """ Get the latest HN Stories. Use the different endpoints to get the
    news items' ids. After that, get the items full objects using another
    helper coroutine.

    Returns
    -------
    ids_list : Tuple
        The result containing a list of ids representing the
    show stories    
    """
    urls = (f"{baseUrl}/topstories.json",       # Get the top stories.
            # Get the latest Ask HN Stories.
            f"{baseUrl}/askstories.json",
            # Get the latest Show HN Stories.
            f"{baseUrl}/showstories.json",
            f"{baseUrl}/jobstories.json",       # Get the latest Job Stories.
            )
    tasks = []

    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.extend(asyncio.ensure_future(query_endpoint(session, url)) )

        # Proceed to get every single news item
        id_list = await asyncio.gather(*tasks)

        all_news_items = get_items_by_id(session, id_list)

    return all_news_items


async def get_items_by_id(session: aiohttp.ClientSession, item_ids: list) -> Tuple:
    """ Get the item using its unique id, an integer value.
    The item can be a Story, Comment, Job, Ask HNs or Poll. The function creates
    Futures from the list and gathers their results after asynchronous execution.

    Parameters
    ----------
    session : aiohttp.ClientSession
        The client session object to use http requests

    item_ids : Tuple
        The list of ids used to fetch the news item

    Returns
    -------
    news_items : Any item
        The responses from the server after executing the created futures.
    """

    tasks = []

    for id in item_ids:
        url = f"{baseUrl}/item/{id}.json"
        tasks.append(asyncio.ensure_future(
            query_endpoint(session=session, url=url)))

    news_items = await asyncio.gather(*tasks)

    return news_items


async def query_endpoint(session: aiohttp.ClientSession, url: str):
    """ Try to get a news_item from an API endpoint, url. This operation
    is asynchronous, to take advantage of concurrency.

    Parameters
    ----------
    session : aiohttp.ClientSession
        The session object is used to query the endpoint.
    url : str
        This parameter holds the endpoint to be queried.

    Returns
    -------
    new_item : Any
        The response from the server, in json format
    """

    async with session.get(url) as response:
        news_item = await response.json()

    return news_item


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_latest_stories())
