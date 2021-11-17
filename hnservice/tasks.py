# This script is used to run api calls to the Hacker News service
# It gets the latest news
import requests

# Scheduler's modules
import asyncio
from background_task import background, tasks
from background_task.models import Task
from datetime import datetime, timedelta
import pytz

# Initialize logging
import logging
file_logger = logging.getLogger(__name__)

from .db_service import DBchecker, DBWriter
from .api_service import get_all_latest_stories, get_latest_story


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
    if checker.is_tables_populated():
        response = asyncio.run(get_latest_story())
        file_logger.info(response)

        # if response:
        #     writer.write_item_to_db(response)

    # Otherwise, get and process latest 100 records
    else:
        latest_stories = asyncio.run(get_all_latest_stories())


def start_task():
    """ Schedule the background function, get_latest_news
    Make sure to run only one scheduled function
    """

    TASK_DURATION = 300

    tasks = Task.objects.filter(verbose_name="Get Latest News")
    if len(tasks) == 0:

        # Schedule to stop after 1 hour
        stop = datetime.utcnow().replace(tzinfo=pytz.utc) + \
            timedelta(hours=1, minutes=0, seconds=0)

        # No task running with this name, call background tasks every 5 minutes
        get_latest_news(schedule=timedelta(seconds=60), repeat=TASK_DURATION,
                                repeat_until=stop, verbose_name="Get Latest News")
        file_logger.debug(f"Scheduling the background task for every {TASK_DURATION/60} minutes")
