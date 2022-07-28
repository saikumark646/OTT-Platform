from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Avg
from django.db.models.signals import post_save
from django.conf import settings
# Create your models here.
# from django.contrib.auth import get_user_model
# User = get_user_model()
User = settings.AUTH_USER_MODEL

class RatingQueryset(models.QuerySet):
    def rating(self):
        return self.aggregate(avg = Avg('value'))['avg']
class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQueryset(self.model,using = self._db)
    
class Rating(models.Model):
    rating_choices = (
        (0,'Zero'),
        (1,'ONE'),
        (2,'TWO'),
        (3,'THREE'),
        (4,'FOUR'),
        (5,'FIVE')
)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(blank=True, null=True,
                            choices =rating_choices, default = 5)
    content_type= models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    objects = RatingManager()

        
    def __str__(self):
        return f' Rating for {self.content_object}'
    
def rating_post_save(sender,instance,created,*args, **kwargs):
    if created:
        content_type = instance.content_type
        object_id = instance.object_id
        user = instance.user
        pk = instance.pk
        qs=Rating.objects.filter(content_type=content_type,
                                object_id=object_id,
                                user=user).exclude(pk=pk)
        if qs.exists():
            qs.delete()
post_save.connect(rating_post_save,sender=Rating)
