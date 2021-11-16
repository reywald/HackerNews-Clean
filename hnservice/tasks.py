# This script is used to run api calls to the Hacker News service
# It gets the latest news
import requests

# Scheduler's modules
from background_task import background, tasks
from background_task.models import Task
from datetime import datetime, timedelta
import pytz
import functools

from .db_service import DBchecker, DBWriter
from .api_service import get_latest_stories, get_latest_story


baseUrl = "https://hacker-news.firebaseio.com/v0"
checker = DBchecker()
writer = DBWriter()


@background(schedule=60)
def get_latest_news():
    """ Get the latest news or populate the news tables first. This 
    function is scheduled to run every 5 minutes.
    """

    # Get most recent news if tables are populated
    # Check if db tables are populated
    db_states = checker.check_dbs()
    is_tables_populated = functools.reduce(
        lambda prop1, prop2: db_states[prop1] or db_states[prop2])
    if is_tables_populated:
        response = get_latest_story()

        # if response:
        #     writer.write_item_to_db(response)

    # Otherwise, get and process latest 100 records
    else:        
        latest_stories = get_latest_stories()



def connect(url):
    """ Try to connect to the API endpoint. Traverse through all 
    possible exceptions

    Returns
    -------
    Response
        The response from the server
    """

    try:
        response = requests.get(url, timeout=10)
        return response

    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error:\n\t{http_error}")
    except requests.exceptions.ConnectionError as conn_error:
        print(f"Connection Error:\n\t{conn_error}")
    except requests.exceptions.RequestException as req_error:
        print(f"Other error:\n\t{req_error}")


def start_task():
    """ Schedule the background function, get_latest_news
    Make sure to run only one scheduled function
    """

    tasks = Task.objects.filter(verbose_name="Get Latest News")
    if len(tasks) == 0:

        # Schedule to stop after 1 hour
        stop = datetime.utcnow().replace(tzinfo=pytz.utc) + \
            timedelta(hours=1, minutes=0, seconds=0)

        # No task running with this name, call background tasks every 5 minutes
        get_latest_news(schedule=timedelta(seconds=60), repeat=300,
                        repeat_until=stop, verbose_name="Get Latest News")
