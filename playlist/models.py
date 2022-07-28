from django.db import models
from django.forms import SelectDateWidget
from django.http import QueryDict
from videos.models import Video
from django.utils import timezone
from django.utils.text import slugify
from categories.models import Categories
from django.contrib.contenttypes.fields import GenericRelation
from tags.models import TaggedItem
from ratings.models import Rating
from django.db.models import Avg,Max,Min,Q
import string
import random
# Create your models here.

class PlaylistQueryset(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state = 'published',
                        publish_timestamp__lte=now) 
    
    def search(self,query = None):
        if query is None:
            return self.none
        return self.filter(
            
            Q(title__icontains = query) | 
            Q(description__icontains = query) | 
            Q(categories__title__icontains = query) |
            Q(categories__slug__icontains = query) |
            Q(tags__tag__icontains = query) 
        ).distinct() #distinct will remove duplicate values
        
    def get_movie_or_show(self):
        return self.filter(
            Q(type = 'MOV') | 
            Q(type = 'TVS') )
    
class PlaylistManage(models.Manager):
    def get_queryset(self):
        return  PlaylistQueryset(self.model,using =self._db)
    
    def published(self):
        return self.get_queryset().published()
    def featured_playlist(self):
        return self.get_queryset().filter(type = 'PLY')
            
class PlayList(models.Model):
    category_choices = (
        ('published','Published'),('draft','Draft')
    )
    playlist_choices = (
        ('MOV','Movie'),('PLY','Playlist'),('TVS','Tv Show'),('SEA','Season')
    )
    parent = models.ForeignKey('self',null = True,blank=True, on_delete =models.SET_NULL)
    related = models.ManyToManyField("self",blank = True,related_name='related',through='PlaylistRelated')
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=30)
    categories =  models.ForeignKey(Categories,on_delete = models.SET_NULL,null = True,blank =True)
    type = models.CharField(max_length = 3,choices=playlist_choices,default = 'PLY')
    video = models.ForeignKey(Video,blank = True,null = True,on_delete = models.SET_NULL,related_name='playlist_featured')
    videos = models.ManyToManyField(Video, blank = True,related_name='playlist_item',through='PlaylistItem')
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True, null=True)
    active =  models.BooleanField(default = False)
    state  =models.CharField(max_length=10,choices=category_choices,default = 'draft')
    tags = GenericRelation(TaggedItem,related_query_name = 'playlist')
    ratings = GenericRelation(Rating,related_query_name = 'playlist')
    
    objects = PlaylistManage()
    
    def __str__(self):
        return self.title
    
    def get_related_items(self):
        return self.playlistrelated_set.all()
    
    def get_absolute_url(self):
        if self.is_movie:
            return f'/playlist/mov/{self.slug}/'
        if self.is_show:
            return f'/playlist/show/{self.slug}/'
        if self.is_season:
            return f'/playlist/show/{self.parent.slug}/{self.slug}/'
        return '/playlist/'
        
    
    
    @property
    def is_movie(self):
        return self.type == 'MOV'
    @property
    def is_season(self):
        return self.type == 'SEA'
    @property
    def is_show(self):
        return self.type == 'TVS'
    
    def get_rating_avg(self):
        return PlayList.objects.filter(id = self.id).aggregate(
                                avg = Avg('ratings__value'))
        
    def get_rating_spread(self):
        return PlayList.objects.filter(id = self.id).aggregate(
                                max = Max('ratings__value'),
                                min = Min('ratings__value')
                            )
    
    @property
    def is_published(self):
        return bool(self.active and self.state == 'published' )
    
    def get_rand_string(self,size = 4, chrs = string.ascii_lowercase+string.digits):
        return ''.join([random.choice(chrs) for _ in range(size)])
    
    def save(self,*args, **kwargs):
        if self.state == 'published' and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.state == 'draft':
            self.publish_timestamp = None
        new_slug = slugify(self.title)+self.get_rand_string()
        qs1 = PlayList.objects.filter(slug = self.slug,
                                    parent = self.parent)
        if qs1.exists() and not self.slug:
            self.slug = new_slug
        elif self.slug is None:
            self.slug = new_slug 
        super().save(*args, **kwargs)

    def get_video_id(self): #get main video id to render video for user 
        return None if self.video is None else self.video.get_video_id()

    def get_clips(self): #get clips to render clips for user 
        return self.playlistitem_set.all().published()

class MovieProxyManage(PlaylistManage):
    def all(self):
        return self.get_queryset().filter(type = 'MOV' )
class MovieProxy(PlayList):
    objects = MovieProxyManage()
    class Meta:
        proxy = True
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        
    def save(self,*args, **kwargs):
        self.type = 'MOV'
        super().save(*args, **kwargs)

    def get_movie_id(self): 
        return self.get_video_id()

class TvShowProxyManage(PlaylistManage):
    def all(self):
        return self.get_queryset().filter(type = 'TVS' )
class TvShowProxy(PlayList):
    objects = TvShowProxyManage()
    class Meta:
        proxy = True
        verbose_name = 'Tv Show'
        verbose_name_plural = 'Tv Shows'
        
    def save(self,*args, **kwargs):
        self.type = 'TVS'
        super().save(*args, **kwargs)
        
    def seasons(self):
        return self.playlist_set.published()
    
    def get_short_display(self):
        return f' has {self.playlist_set.count()} Seasons'

class TvShowSeasonProxyManager(PlaylistManage):
    def all(self):
        return self.get_queryset().filter(type = 'SEA')
class TvShowSeasonProxy(PlayList):
    objects = TvShowSeasonProxyManager()
    class Meta:
        proxy = True
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
    def save(self,*args, **kwargs):
        self.type = 'SEA'
        super().save(*args, **kwargs)
        
    def get_season_trailer(self):
        return self.get_video_id()
    def get_episodes(self):
        return self.playlistitem_set.all().published()



class PlaylistItemQueryset(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(playlist__state = 'published',
                            playlist__publish_timestamp__lte=now,
                            video__state = 'published',
                            video__publish_timestamp__lte=now)
class PlaylistItemManage(models.Manager):
    def get_queryset(self): 
        return  PlaylistItemQueryset(self.model,using =self._db)
    
    def published(self):
        return self.get_queryset().published()

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(PlayList,on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    order =models.IntegerField(default = 1)
    objects = PlaylistItemManage()
    
    class Meta:
        ordering = ['order','-timestamp']

def pr_limit_choices_to():
    return Q(type = 'MOV') | Q(type = 'TVS')
    
class PlaylistRelated(models.Model):
    playlist = models.ForeignKey(PlayList,on_delete=models.CASCADE)
    related = models.ForeignKey(PlayList,on_delete=models.CASCADE,related_name='related_item' , limit_choices_to = pr_limit_choices_to)
    timestamp = models.DateTimeField(auto_now_add=True)
    order =models.IntegerField(default = 1)


"""   
In [4]: obj =  PlayList.objects.first()
In [5]: obj
Out[5]: <PlayList: playlist test>

In [6]: obj.get_rating_avg()
Out[6]: {'avg': 4.666666666666667}

In [7]: obj.get_rating_spread()
Out[7]: {'max': 5, 'min': 3}


Aggregate:
obj = PlayList.objects.get(id = 1)  # it return Model
obj
<PlayList: playlist test> 

type(obj)
playlist.models.PlayList 
obj.aggregate(Avg('ratings__value'))
'PlayList' object has no attribute 'aggregate' "ERROR"
(aggregate atttribule is Queryset level)
In [11]: obj1 = PlayList.objects.filter(id = 1)

In [12]: obj1
Out[12]: <PlaylistQueryset [<PlayList: playlist test>]>
In [13]: obj1.get_rating_avg()
'PlaylistQueryset' object has no attribute 'get_rating_avg' "ERROR"
(get_rating_avg function is model level)
obj1 = PlayList.objects.filter(id = 1) # it returns queryset
obj1
<PlaylistQueryset [<PlayList: playlist test>]>

obj1.aggregate(Avg('ratings__value'))
{'ratings__value__avg': 4.666666666666667}

type(obj1)
playlist.models.PlaylistQueryset
        
    
    
        
>>>>>>>>>>>>>>>>>>>       

In []: obj1 = PlayList.objects.get(id = 3)
In [6]: obj1.videos.all()
Out[6]: <VideoQueryset [<Video: Balck Panther>, <Video: Thor>, <Video: Avangers>]>
In [7]: obj1.video
Out[7]: <Video: Avangers>
In []: qs  = obj1.playlistitem_set.all()
In []: qs
Out[]: <QuerySet [<PlaylistItem: PlaylistItem object (2)>, <PlaylistItem: PlaylistItem object (3)>, <PlaylistItem: PlaylistItem object (4)>]>

In [11]: obj1.playlistitem_set.all().order_by('-order')
Out[11]: <QuerySet [<PlaylistItem: PlaylistItem object (4)>, <PlaylistItem: PlaylistItem object (3)>, <PlaylistItem: PlaylistItem object (2)>]>

In [15]: qs.values('video')
Out[15]: <QuerySet [{'video': 4}, {'video': 5}, {'video': 3}]>

In [17]: qs.values('video') #video ids will print
Out[17]: <QuerySet [{'video': 4}, {'video': 5}, {'video': 3}]>

In [18]: qs.values('playlist')
Out[18]: <QuerySet [{'playlist': 3}, {'playlist': 3}, {'playlist': 3}]>

In [19]: qs.values('order') 
Out[19]: <QuerySet [{'order': 1}, {'order': 2}, {'order': 3}]>

>>>>>>>>>>
obj1 = PlaylistItem.objects.all().first()
In [7]: obj1.video
Out[7]: <Video: Avangers>

In [11]: obj1.playlist
Out[11]: <PlayList: test3>

In [12]: obj1.order
Out[12]: 1

In [13]: obj1.video.id
Out[13]: 3
In [15]: Video.objects.filter(id = 3)
Out[15]: <VideoQueryset [<Video: Avangers>]>

In [21]: obj
Out[21]: <PlayList: the office series>

In [22]: obj1
Out[22]: <PlayList: the office series season 2>

In [23]: obj1.parent
Out[23]: <PlayList: the office series>

In [24]: obj.playlist_set.all().last()
Out[24]: <PlayList: the office series season 2>

In [25]: obj.playlist_set.all().all()
Out[25]: <PlaylistQueryset [<PlayList: the office series season 1>, <PlayList: the office series season 2>]>

>>>>>>>>>>>>>
here show is parent object and season is child object,

to get th parent detail by using child, child.parent
to get the chil details by using parent parent.playlist_set.all() or parent.<ForeignKeyObj_set.all()
In [21]: show
Out[21]: <PlayList: the office series>

In [22]: season
Out[22]: <PlayList: the office series season 2>

In [23]: season.parent
Out[23]: <PlayList: the office series>

In [24]: show.playlist_set.all().last()
Out[24]: <PlayList: the office series season 2>

In [25]: show.playlist_set.all()
Out[25]: <PlaylistQueryset [<PlayList: the office series season 1>, <PlayList: the office series season 2>]>
"""