from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import pre_save
# Create your models here.

class TaggedItemManager(models.Manager):
    def unique_list(self):
        tags_set = set(self.get_queryset().values_list('tag',flat = True))
        return sorted(list(tags_set))

class TaggedItem(models.Model):
    tag = models.SlugField(blank=True, null=True)
    content_type= models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    objects = TaggedItemManager()
    
    @property
    def slug(self):
        return self.tag
    def __str__(self):
        return self.tag

def lowercase_tag_pre_save(sender,instance,*args, **kwargs):
    instance.tag = f"{instance.tag}".lower()
pre_save.connect(lowercase_tag_pre_save,sender=TaggedItem)







""" 
Accessing ContentType objects
In [17]: cont_type =ContentType.objects.get(app_label = 'playlist',model = 'playlist')
In [18]: cont_type
Out[18]: <ContentType: playlist | play list>

In [19]: cont_type.model_class()
Out[19]: playlist.models.PlayList

In [20]: model = cont_type.model_class()

In [21]: model.objects.all()
Out[21]: <PlaylistQueryset [<PlayList: playlist test>, <PlayList: playlist test2>, <PlayList: the office series season 1>, <PlayList: the office series season 2>, <PlayList: the office series>, <PlayList: season 3>, <PlayList: prince of pertia>, <PlayList: new movie>, <PlayList: Season 4>]>

In [22]: model.objects.filter(type = 'SEA')
Out[22]: <PlaylistQueryset [<PlayList: the office series season 1>, <PlayList: the office series season 2>, <PlayList: season 3>, <PlayList: Season 4>]>
"""            
            
            