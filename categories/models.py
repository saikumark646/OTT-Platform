from django.db import models
from django.utils.text  import slugify
# Create your models here.
from django.contrib.contenttypes.fields import GenericRelation
from tags.models import TaggedItem

class  Categories(models.Model):
    title = models.CharField(max_length=10)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = GenericRelation(TaggedItem,related_query_name = 'category')
    
    def get_absolute_url(self):
        return f'/cat/{self.slug}/'
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural  = 'Categories'
    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)