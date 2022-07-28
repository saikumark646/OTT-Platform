from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.db.models import Count

from playlist.models import PlayList
from .models import Categories
from playlist.mixins import PlaylistMixin
# Create your views here.


class CategoryListView(ListView):
    queryset = Categories.objects.all().filter(active=True).annotate(pl_count = Count('playlist')).filter(pl_count__gt=0)
    
    
class CategoryDetailView(PlaylistMixin,ListView):
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data()
        try:
            slug = self.kwargs.get('slug')
            obj = Categories.objects.get(slug = slug)
        except Categories.DoesNotExist as e:
            raise Http404 from e
        except Categories.MultipleObjectsReturned as e:
            raise Http404 from e
        context['object'] = obj
        if obj is not None:
            context['title'] = obj.title
        return context
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return PlayList.objects.filter(categories__slug = slug)
