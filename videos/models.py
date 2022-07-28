from weakref import proxy
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.

# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager,self).get_queryset().filter(state = 'published')


class VideoQueryset(models.QuerySet):
    def published(self):
        now = timezone.now
        return self.filter(state = 'published',
                        publish_timestamp__lte=now)
    
class VideoManage(models.Manager):
    def get_queryset(self):
        return VideoQueryset(self.model,using = self._db)
    def published(self):
        return self.get_queryset().published()
    
    
    
class Video(models.Model):
    category_choices = (
        ('published','Published'),('draft','Draft')
    )
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True, null=True)
    active =  models.BooleanField(default = False)
    state  =models.CharField(max_length=10,choices=category_choices,default = 'draft')
    objects = VideoManage()

    def __str__(self):
        return self.title
    
    @property
    def is_published(self):
        return bool(self.active and self.state == "published")
    
    def get_video_id(self):
        return self.video_id if self.is_published else None

# def get_playlist_ids(self):
    #     return list(self.playlist_featured.all().values_list('id',flat = True))
    # if we didnt set related name in playlists have to use playlist_set for reverse relationship
    def save(self,*args, **kwargs):
        if self.state == 'published' and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.state == 'draft':
            self.publish_timestamp  = None
        
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All video'
        verbose_name_plural = 'All videos'


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'published video'
        verbose_name_plural = 'published videos'
        
#using django signals   
# def slugify_pre_save(self,instance,*args, **kwargs):
#     slug = instance.slug
#     if slug is None:
#         title  = instance.title
#         instance.slug = slugify(title)
# pre_save.connect(slugify_pre_save, sender = Video)

""" with video playlist details is rendered
>>> obj = Video.objects.get(id = 23)
>>> obj
<Video: test video>
>>> dir(obj)
>>> obj.playlist_item.all()
<PlaylistQueryset [<PlayList: test>, <PlayList: test play>, <PlayList: test2>]>
>>> obj.playlist_featured.all()
<PlaylistQueryset [<PlayList: test2>]>
"""