from django.contrib import admin
from .models import (
    Comment, Job, Poll, PollOption, Story, User
)

admin.site.register([Comment, Job, Poll, PollOption, Story, User])
