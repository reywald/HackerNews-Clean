from django.db import models
from django.test import TestCase

from .models import Comment, Job, Poll, PollOption, Story, User


class HomePageTests(TestCase):
    """ Test the homepage functionality"""

    def setUp(self):
        pass

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_contents(self):
        response = self.client.get("/")
        self.assertContains(response, "Hacker News")

    def test_home_page_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ModelsTests(TestCase):
    """ Test the models """

    def setUp(self):
        self.user = User.objects.create(**{
            "id": "jl",
            "delay": 0,
            "created": 1173923446,
            "karma": 2937,
            "about": "This is a test",
            "submitted": [8265435, ]
        })

    def test_dict_can_create_user(self):
        self.assertEqual(self.user.id, "jl")
        self.assertEqual(self.user.about, "This is a test")

    def test_story_references_user(self):
        params = {
            "by": self.user,
            "descendants": 71,
            "id": 8863,
            "kids": [
                8952,
                8876
            ],
            "score": 11122223,
            "time": 1175714200,
            "title": "Prism. The perfect OAS (Swagger) companion.",
            "type": "story",
            "url": "http://stoplight.io/prism/"
        }
        story = Story.objects.create(**params)
        self.assertEqual(story.by, self.user)
        self.assertEqual(story.by.id, 'jl')

    def test_job_references_user(self):
        params = {
            "id": 192327,
            "by": self.user,
            "score": 6,
            "text": "Justin.tv is the biggest live video site online. We serve hundreds of thousands of video streams a day, and have supported up to 50k live concurrent viewers. Our site is growing every week, and we just added a 10 gbps line to our colo. Our unique visitors are up 900% since January.<p>There are a lot of pieces that fit together to make Justin.tv work: our video cluster, IRC server, our web app, and our monitoring and search services, to name a few. A lot of our website is dependent on Flash, and we're looking for talented Flash Engineers who know AS2 and AS3 very well who want to be leaders in the development of our Flash.<p>Responsibilities<p><pre><code>    * Contribute to product design and implementation discussions\n    * Implement projects from the idea phase to production\n    * Test and iterate code before and after production release \n</code></pre>\nQualifications<p><pre><code>    * You should know AS2, AS3, and maybe a little be of Flex.\n    * Experience building web applications.\n    * A strong desire to work on website with passionate users and ideas for how to improve it.\n    * Experience hacking video streams, python, Twisted or rails all a plus.\n</code></pre>\nWhile we're growing rapidly, Justin.tv is still a small, technology focused company, built by hackers for hackers. Seven of our ten person team are engineers or designers. We believe in rapid development, and push out new code releases every week. We're based in a beautiful office in the SOMA district of SF, one block from the caltrain station. If you want a fun job hacking on code that will touch a lot of people, JTV is for you.<p>Note: You must be physically present in SF to work for JTV. Completing the technical problem at <a href=\"http://www.justin.tv/problems/bml\" rel=\"nofollow\">http://www.justin.tv/problems/bml</a> will go a long way with us. Cheers!",
            "time": 1210981217,
            "title": "Justin.tv is looking for a Lead Flash Engineer!",
            "type": "job",
            "url": ""
        }
        job = Job.objects.create(**params)
        self.assertEqual(job.by, self.user)
        self.assertEqual(self.user.job_set.count(), 1)

    def test_poll_references_user(self):
        poll = Poll.objects.create(**{
            "by": self.user,
            "descendants": 54,
            "id": 126809,
            "kids": [
                126822,
                126823,
                126993, ],
            "parts": [
                126810,
                126811,
                126812
            ],
            "score": 46,
            "text": "",
            "time": 1204403652,
            "title": "Poll: What would happen if News.YC had explicit support for polls?",
            "type": "poll"
        })
        self.assertEqual(poll.by, self.user)
        self.assertEqual(self.user.poll_set.count(), 1)

    def test_story_can_create_comment(self):
        story = Story.objects.create(
            **{
                "by": self.user,
                "id": 8863,
                "score": 11122223,
                "time": 1175714200,
                "title": "Prism. The perfect OAS (Swagger) companion.",
                "type": "story",
                "url": "http://stoplight.io/prism/"
            }
        )
        story.comments.create(
            **{
                "by": self.user,
                "id": 2921983,
                "parent": story,
                "text": "Aw shucks, guys ... you make me blush with your compliments.<p>Tell you what, Ill make a deal: I'll keep writing if you keep reading. K?",
                "time": 1314211127,
                "type": "comment"
            }
        )
        
        self.assertEqual(story.comments.count(), 1)
