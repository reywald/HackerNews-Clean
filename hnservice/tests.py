from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from hnservice.api_service import get_news_item, get_top_stories
from django.test import TestCase
from django.db import IntegrityError

from .db_service import DBchecker
from news.models import Comment, Job

# Create your tests here.


class TestAsyncService(AioHTTPTestCase):

    async def get_application(self):
        return web.Application()

    @unittest_run_loop
    async def test_get_news_item_returns_item(self):
        url = "https://hacker-news.firebaseio.com/v0/maxitem.json"
        response = await get_news_item(self.client, url)
        assert response is not None

    @unittest_run_loop
    async def test_get_latest_news_gets_top_stories(self):
        responses = await get_top_stories()
        assert responses is not None


class TestDBCheckerService(TestCase):

    def setUp(self) -> None:
        self.db_checker = DBchecker()

    def test_tables_are_empty_returns_false(self):
        is_not_empty = self.db_checker.check_dbs()
        self.assertEqual(is_not_empty, False)

    def test_tables_with_data_returns_true(self):
        # Add a record to the Comment table
        comment = Comment(id=1, parent=0, by='Gunax',
                          text="This is required concept", time=1633544861, type='comment')
        comment.save()

        is_not_empty = self.db_checker.check_dbs()
        self.assertEqual(is_not_empty, True)


class TestDBWriterService(TestCase):

    def setUp(self) -> None:
        self.news_item = Comment.objects.create(id=1, parent=0, by='Gunax',
                                                text="This is required concept", time=1633544861, type='comment')

    def test_comment_table_populated(self):
        self.assertEqual(1, Comment.objects.count())
        self.assertEqual(Comment.objects.first(), self.news_item)

    def test_use_dict_to_populate_table(self):
        # Arrange
        job_dict = {"id": 1, "title": "The Test", "by": "Gunar",
                    "text": "This is a test", "time": 163346732, "type": "job"}
        Job.objects.create(**job_dict)

        # Act & Assert
        job = Job.objects.get(id=1)
        self.assertEqual(job.id, job_dict["id"])
        self.assertEqual(job.title, job_dict["title"])
        self.assertEqual(job.text, job_dict["text"])

    def test_insert_same_record_again_raises_Exception(self):
        # Arrange
        another_comment = {"id": 1, "parent": 0, "by": 'Gunax',
                           "text": "This is required concept", "time": 1633544861, "type": 'comment'}

        # Act & Assert
        with self.assertRaises(IntegrityError) as error:
            Comment.objects.create(**another_comment)

        self.assertIn("UNIQUE constraint failed", str(error.exception))
