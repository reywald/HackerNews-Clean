from django.core.exceptions import FieldDoesNotExist
from django.db import models, IntegrityError, DatabaseError
from news.models import Comment, Job, Poll, PollOption, Story
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")


class DBchecker():
    """
    Used by the HN Service to check if the tables are populated

    Methods
    -------
    check_dbs()
        Checks each model (Story, Job, Poll, Comment) for any recoreds.
    """

    def check_dbs(self):
        """ Check if data is in tables by fetching first rows 

        Returns
        -------
        {'item_type': bool}
            Whether any of the 5 QuerySets are empty or populated
        """
        db_states = {'comment': False, 'job': False,
                     'poll': False, 'polloption': False, 'story': False}

        db_states['comment'] = Comment.objects.all().first() is not None
        db_states['job'] = Job.objects.all().first() is not None
        db_states['poll'] = Poll.objects.all().first is not None
        db_states['polloption'] = PollOption.objects.all().first is not None
        db_states['story'] = Story.objects.all().first() is not None

        logging.info("Checking the tables for any data")

        return db_states


class DBWriter():
    """
    Handles writing to the various tables
    ...

    Methods
    -------
    write_item_to_db(news_item: dict)
        Check the type of item: job, story, comment, poll, pollopt
    and delegate to the relevant function, which writes to the 
    proper database table

    __create_entry(news_item: dict, dataset: model.QuerySet)
        Commits the contents of the new_item dictionary object to
    its appropriate table. We have Job, Story, Comment, Poll & 
    Poll Option models. 
    Example: __create_entry(news_item, self.__job) writes the news_item to
    the Job table
    """

    def __init__(self) -> None:
        self.__comment = Comment.objects.all()
        self.__job = Job.objects.all()
        self.__poll = Poll.objects.all()
        self.__poll_options = PollOption.objects.all()
        self.__story = Story.objects.all()

    def write_item_to_db(self, news_item: dict):
        """ Check the type of item: job, story, comment, poll, pollopt
        and delegate to the relevant function, which writes to the 
        proper database table

        Parameters
        ----------
        news_item : dict
            The record to write to the database table
        """

        if news_item["type"] == 'job' and self.__has_same_structure(Job, news_item):
            self.__create_entry(news_item, self.__job)

        elif news_item["type"] == 'comment' and self.__has_same_structure(Comment, news_item):
            self.__create_entry(news_item, self.__comment)

        elif news_item["type"] == 'poll' and self.__has_same_structure(Poll, news_item):
            self.__create_entry(news_item, self.__poll)

        elif news_item["type"] == 'pollopt' and self.__has_same_structure(PollOption, news_item):
            self.__create_entry(news_item, self.__poll_options)

        elif news_item["type"] == 'story' and self.__has_same_structure(Story, news_item):
            self.__create_entry(news_item, self.__story)

    def __create_entry(self, news_item: dict, dataset: models.QuerySet):
        """ Tries to insert an entry into its relevant model. Uses 
        get_or_create() to check if it already exists or not. IntegrityError
        or DatabaseError are captured and handled in an edge-case

        Parameters
        ----------
        news_item : dict
            The dictionary object containing the entry to search or create
        dataset : models.QuerySet
            This QuerySet provides the lookup method get_or_create().
        """

        try:
            dataset.get_or_create(**news_item)

        except IntegrityError:
            logging.exception(
                f"Could not create entry {news_item.id}. Entry already exists")

        except DatabaseError as db_error:
            logging.exception(f"Other error:\n\t{db_error}")

    def __has_same_structure(self, item_model: models.Model, item_dict: dict):
        """ Check if the dictionary objects keys are also in the 
        model's fields' list

        Return
        ------
        bool
            Whether both structures are compatible
        """

        for key in item_dict:
            try:
                item_model._meta.get_field(key)
            except FieldDoesNotExist:
                logging.exception(
                    f"{item_dict['id']}'s {key} is not a field in {item_model._meta.label}")
                return False

        return True
