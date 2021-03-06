from typing import Tuple
import aiohttp
import asyncio

# Initialize logging
import logging
file_logger = logging.getLogger(__name__)

baseUrl = "https://hacker-news.firebaseio.com/v0"


async def get_latest_story() -> Tuple:
    """ Get the most recent news item 

    Returns
    -------
    item : dict
        The result which is a dictionary converted from a json object.
    """
    url = f"{baseUrl}/maxitem.json"

    async with aiohttp.ClientSession() as session:
        response = await query_endpoint(session, url)

        if response:
            item = await get_item_details(session, response)

    return item


async def get_all_latest_stories() -> Tuple:
    """ Get the latest HN Stories. Use the different endpoints to get the
    news items' ids. After that, get the items full objects using another
    helper coroutine.

    Returns
    -------
    ids_list : Tuple
        The result containing a list of ids representing the show stories    
    """
    file_logger.info("*" * 30 + "Get all latest stories" + "*" * 30)
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
            tasks.append(asyncio.ensure_future(query_endpoint(session, url)))

        # Proceed to get every single news item
        id_list = await asyncio.gather(*tasks)

        all_news_items = await get_items_by_id(session, id_list)

    return all_news_items


async def get_items_by_id(session: aiohttp.ClientSession, news_sources: list):
    """ Get the item using its unique id, an integer value.
    The item can be a Story, Comment, Job, Ask HNs or Poll. The function creates
    Futures from the list and gathers their results after asynchronous execution.

    Parameters
    ----------
    session : aiohttp.ClientSession
        The client session object to use http requests

    news_sources : Tuple
        The list of lists of ids of news items to fetch.

    Returns
    -------
    news_items : Any item
        The responses from the server after executing the created futures.
    """

    tasks = [[]] * len(news_sources)
    news_items = [[]] * len(news_sources)

    file_logger.info("*" * 30 + "Get items by id" + "*" * 30)

    for idx, news_source in enumerate(news_sources):
        for item_id in news_source:
            url = f"{baseUrl}/item/{item_id}.json"
            tasks[idx].append(asyncio.ensure_future(
                query_endpoint(session=session, url=url)))

        news_items[idx] = await asyncio.gather(*tasks[idx])

    return news_items


async def get_item_details(session: aiohttp.ClientSession, item):
    """ Get the details of the item from HackNews' server

    Returns
    -------
    Object
        The json-parsed response data
    """
    url = f"{baseUrl}/item/{item}.json"

    response = await query_endpoint(session, url)
    return response


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
        if response.ok:
            file_logger.info(f"{url} - {response.status}")
            return await response.json()
        else:
            file_logger.error(f"{url} - {response.status}")
            return None


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(get_all_latest_stories())
