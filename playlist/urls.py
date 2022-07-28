from django.urls import path
from .views import (MovieProxyListView,TvShowSeasonProxyListView,TvShowProxyListView,PlaylistListView,MovieProxyDetailView,PlaylistDetailView,TvShowProxyDetailView,TvShowSeasonProxyDetailView,SearchView)

app_name = 'playlist'

urlpatterns = [
    path('search/',SearchView.as_view()),
    path('',PlaylistListView.as_view(),name = 'featured_playlist'),
    path('<int:pk>/',PlaylistDetailView.as_view(),name = 'featured_playlist_detail'),
    
    path('mov/',MovieProxyListView.as_view(),name = 'movies'),
    path('mov/<slug:slug>/',MovieProxyDetailView.as_view(),name = 'movies_detail'),
    
    path('show/',TvShowProxyListView.as_view(),name = 'tv_show'),
    path('show/<slug:slug>/',TvShowProxyDetailView.as_view(),name = 'tv_show_detail'),
    
    path('sea/',TvShowSeasonProxyListView.as_view(),name = 'season'),    
    path('show/<slug:showSlug>/<slug:seasonSlug>/',TvShowSeasonProxyDetailView.as_view(),name = 'season_detail'),
    
]
