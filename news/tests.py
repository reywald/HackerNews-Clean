from django.http import response
from django.test import TestCase

# Create your tests here.


class HomePageTests(TestCase):
    """ Test the homepage functionality"""

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_contents(self):
        response = self.client.get("/")
        self.assertContains(response, "Hacker News")

    def test_home_page_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home')
