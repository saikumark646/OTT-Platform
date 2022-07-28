from django.contrib import admin
from playlist.models import PlayList, PlaylistItem,TvShowProxy,TvShowSeasonProxy,MovieProxy,PlaylistRelated
from tags.admin import TaggedItemInline
# Register your models here.

@admin.register(MovieProxy)
class AdminMovieProxy(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ['title','slug','is_published','categories','publish_timestamp','id']
    def get_queryset(self, request):
        return MovieProxy.objects.all()


class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0
    fields = ['order','video']
class AdminTvShowSeasonProxy(admin.ModelAdmin):
    inlines = [TaggedItemInline,SeasonEpisodeInline]
    list_display = ['title','parent','categories','slug', 'video', 'is_published','id']
    
    def get_queryset(self, request):
        return TvShowSeasonProxy.objects.all()
        
admin.site.register(TvShowSeasonProxy,AdminTvShowSeasonProxy)


class TvShowSeasonProxyInline(admin.TabularInline):
    model = TvShowSeasonProxy
    extra = 0
    fields = ['title','order','state']

class AdminTvShowProxy(admin.ModelAdmin):
    inlines = [TaggedItemInline,TvShowSeasonProxyInline]
    list_display = ['title','parent','categories','slug','is_published','state','id']
    fields = ['title','slug','active','video','categories','state','publish_timestamp']
    def get_queryset(self, request):
        return TvShowProxy.objects.all()
    
admin.site.register(TvShowProxy,AdminTvShowProxy)


class PlaylistRelatedInline(admin.TabularInline):
    model = PlaylistRelated
    fk_name = 'playlist'
    extra = 0
    
class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class PlayListAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline,PlaylistRelatedInline,PlaylistItemInline] 
    fields = ['title','slug','description','is_published','state','id']
    list_display = ['title','slug','is_published','state','publish_timestamp','id']
    list_filter = ['active','state','timestamp']
    search_fields = ['title']
    readonly_fields = ['id','is_published'] 
    
    def get_queryset(self, request):
        return PlayList.objects.filter(type = 'PLY')
    class Meta: 
        model = PlayList

admin.site.register(PlayList,PlayListAdmin) 
    
    
    
    
    
    
    

