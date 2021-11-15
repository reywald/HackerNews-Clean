from django.db import models
from django.db.models.query_utils import Q
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class User(models.Model):
    """ Encapsulates HackNews User """

    id = models.CharField(primary_key=True, max_length=100)
    delay = models.PositiveIntegerField(null=True, blank=True)
    created = models.PositiveIntegerField(null=False)
    karma = models.PositiveIntegerField(null=False)
    about = models.CharField(max_length=500, blank=True)
    submitted = models.TextField(blank=True)


class Base(models.Model):
    """ Encapsulates the core generic fields all news items share in common"""

    id = models.PositiveIntegerField(primary_key=True, editable=False)
    deleted = models.BooleanField(default=False)

    COMMENT = 'comment'
    JOB = 'job'
    POLL = 'poll'
    POLLOPT = 'pollopt'
    STORY = 'story'

    ITEM_TYPES = ((COMMENT, 'Comment'),
                  (STORY, 'Story'),
                  (JOB, 'Job'),
                  (POLL, 'Poll'),
                  (POLLOPT, 'Poll Option')
                  )
    type = models.CharField(
        choices=ITEM_TYPES, max_length=15, null=False, default=COMMENT)

    by = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.PositiveIntegerField(null=True, blank=True)
    dead = models.BooleanField(default=False)
    kids = models.TextField(blank=True, null=True)
    text = models.CharField(max_length=5000, blank=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Comment(Base):
    """ Encapsulates a comment. It usually has a Story or Poll parent. 
    Comments can be related to stories or other comments  as indicated 
    by the GenericForeignKey field.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('content_type', 'object_id')

    comments = GenericRelation('Comment')

    def __str__(self) -> str:
        return self.text        # Truncate to 20 words

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})


class Job(Base):
    """ Encapsulates a job news item. """

    score = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField(blank=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})


class Poll(Base):
    """ Encapsulates a poll. It has related poll options. """

    descendants = models.PositiveSmallIntegerField(null=True, blank=True)
    parts = models.TextField(null=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("poll_detail", kwargs={"pk": self.pk})


class PollOption(Base):
    """ Encapsulates a poll option. It belongs to a parent Poll. """

    parent = models.ForeignKey(Poll, on_delete=models.CASCADE,
                               limit_choices_to=Q(type='Poll'))
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.text

    def get_absolute_url(self):
        return reverse("poll_option_detail", kwargs={"pk": self.pk})


class Story(Base):
    """ Encapsulates a story news item. It has related comments. """

    comments = GenericRelation(Comment)
    descendants = models.PositiveSmallIntegerField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("story_detail", kwargs={"pk": self.pk})
