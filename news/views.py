from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import Comment, Job, Poll, PollOption, Story

from itertools import chain


class HomePageView(TemplateView):
    """ Renders the home page 

    Parameters
    ----------
    template_name : The name of the template .html file to use
    """
    template_name = "index.html"


class BaseListView(ListView):
    paginate_by = 5
    template_name = 'list.html'
    ordering = '-id'
    heading_type = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_heading'] = self.heading_type
        context['news_types'] = {
            'all_news': "All News", 'jobs': "Jobs", 'polls': "Polls", 'stories': "Stories"}

        return context


class NewsListView(BaseListView):
    heading_type = 'All News'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['jobs'] = Job.objects.all()
        context['polls'] = Poll.objects.all()
        context['polloptions'] = PollOption.objects.all()
        context['stories'] = Story.objects.all()

        return context

    def get_queryset(self):
        comments = Comment.objects.all()
        jobs = Job.objects.all()
        polls = Poll.objects.all()
        polloptions = PollOption.objects.all()
        stories = Story.objects.all()

        return sorted(chain(comments, jobs, polls, polloptions, stories), key=lambda item: item.id, reverse=True)


class SearchListView(BaseListView):
    heading_type = "Search Results"
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get('search')

        comments = Comment.objects.filter(text__icontains=query)
        jobs = Job.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query))
        polls = Poll.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query))
        polloptions = PollOption.objects.filter(text__icontains=query)
        stories = Story.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query))

        return sorted(chain(comments, jobs, polls, polloptions, stories), key=lambda item: item.id)


class CommentListView(BaseListView):
    model = Comment
    heading_type = 'Comments'


class CommentDetailView(DetailView):
    model = Comment
    template_name = 'detail.html'


class JobListView(BaseListView):
    model = Job
    heading_type = 'Jobs'


class JobDetailView(DetailView):
    template_name = 'detail.html'
    model = Job


class PollListView(BaseListView):
    model = Poll
    heading_type = 'Polls'


class PollDetailView(DetailView):
    template_name = 'detail.html'
    model = Poll


class StoryListView(BaseListView):
    model = Story
    heading_type = 'Stories'


class StoryDetailView(DetailView):
    template_name = 'detail.html'
    model = Story
