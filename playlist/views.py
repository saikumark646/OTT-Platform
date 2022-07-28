from django.shortcuts import render
from .models import PlayList,MovieProxy,TvShowProxy,TvShowSeasonProxy
from django.views.generic import ListView,DetailView
from django.utils import timezone 
from .mixins import PlaylistMixin
# Create your views here.

# def MovieListView(request):
#     qs = MovieProxy.objects.all()
#     return render(request, 'base.html', {'qs':qs})

class SearchView(PlaylistMixin,ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        query = self.request.GET.get("q")
        if query is not None:
            context['title'] = f"search for {query}"
        else:
            context['title'] = "search something!!!"
        return context
    
    def get_queryset(self):
        query  =self.request.GET.get("q")  # request.GET = {}
        return PlayList.objects.all().search(query = query)


class PlaylistListView(PlaylistMixin,ListView):
    template_name = 'playlist/featured_list.html'
    queryset = PlayList.objects.featured_playlist()
    title = "Featured"

class PlaylistDetailView(PlaylistMixin,DetailView):
    template_name = 'playlist/playlist_detail.html'
    queryset = PlayList.objects.featured_playlist()
    title = "Featured"
    
    # def get_object(self): 
    #     #  if we give pk in urls no need to define get_object
    #     request = self.request
    #     kwargs = self.kwargs
    #     return self.get_queryset().first()

class MovieProxyListView(PlaylistMixin,ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies" 

class MovieProxyDetailView(PlaylistMixin,DetailView):
    template_name = 'playlist/movie_detail.html'
    queryset = MovieProxy.objects.all()
    title = "Movies"

class TvShowProxyListView(PlaylistMixin,ListView):
    queryset = TvShowProxy.objects.all()
    title = 'TV Show'
    
class TvShowProxyDetailView(PlaylistMixin,DetailView):
    template_name = 'playlist/tvs_detail.html'
    queryset = TvShowProxy.objects.all()
    title = 'TV Show'  

class TvShowSeasonProxyListView(PlaylistMixin,ListView):
    queryset = TvShowSeasonProxy.objects.all()
    title = 'Season'
    
class TvShowSeasonProxyDetailView(PlaylistMixin,DetailView):
    template_name = 'playlist/sea_detail.html'
    queryset = TvShowSeasonProxy.objects.all()
    title = 'Season'
    
    def get_object(self,*args, **kwargs):
        show_slug = self.kwargs.get('showSlug')
        season_slug = self.kwargs.get('seasonSlug')
        
        #now = timezone.now()
        # try:
        #     obj = TvShowSeasonProxy.objects.get(state = 'published',publish_timestamp__lte = now,
        #     parent__slug__iexact=show_slug,
        #     slug__iexact=season_slug
        #     )
        # except TvShowSeasonProxy.MultipleObjectsReturned:
        #     qs = TvShowSeasonProxy.objects.filter(state = 'published',publish_timestamp__lte = now,
        #     parent__slug__iexact=show_slug,
        #     slug__iexact=season_slug
        #     )
        #     obj = qs.first()
        # return obj
        
        qs = self.get_queryset().filter(parent__slug__iexact=show_slug,
                                        slug__iexact=season_slug)
        if qs.count() == 0:
            raise Exception('not found')
        return qs.first()
        
            
        