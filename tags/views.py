from multiprocessing import context
from django.shortcuts import render
from django.views.generic import ListView,DetailView

from playlist.models import PlayList
# Create your views here.
from .models import TaggedItem
from playlist.mixins import PlaylistMixin

class TaggedItemList(ListView):
    template_name = 'tags/tags_list.html'
    queryset = TaggedItem.objects.unique_list()

class TaggedItemDetail(PlaylistMixin,DetailView):
    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = f"{self.kwargs.get('tag')}".title()
        return context
    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return PlayList.objects.filter(tags__in = tag)