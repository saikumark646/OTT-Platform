    
from django.contrib import admin
from .models import Video, VideoPublishedProxy,VideoAllProxy
# Register your models here.

@admin.register(VideoPublishedProxy)
class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title','slug','video_id']
    list_filter = ['publish_timestamp']
    search_fields = ['title']

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active = True)
        #return VideoPublishedProxy.Published.all()
@admin.register(VideoAllProxy)
class VideoAllProxyAdmin(admin.ModelAdmin):
    list_display = ['title','slug','active','is_published','state','publish_timestamp'] #,'get_playlist_ids']
    list_filter = ['active','state','timestamp']
    search_fields = ['title']
    readonly_fields = ['id','is_published'] #,'get_playlist_ids'] 
    

    # def is_published(self,obj,*args, **kwargs):
    #     return obj.active
#admin.site.register(Video)


