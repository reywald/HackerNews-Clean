from typing import Tuple
import aiohttp
import asyncio

baseUrl = "https://hacker-news.firebaseio.com/v0"


async def get_latest_news() -> Tuple:
    """ Get the latest news.
    Use a Future object of the coroutine to run, then create the 
    aiohttp.ClientSession instance to make API requests.

    Returns
    -------
    news_items : Tuple
        The result of each future object when executed successfully.
    """

    urls = (f"{baseUrl}/topstories.json")
    
    async with aiohttp.ClientSession as session:
        tasks = []

        for url in urls:
            tasks.append(asyncio.ensure_future(
                get_news_item(session=session, url=url)))

        news_items = await asyncio.gather(*tasks)
        
        return news_items


async def get_news_item(session: aiohttp.ClientSession, url: str):
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
