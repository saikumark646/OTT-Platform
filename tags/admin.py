from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import TaggedItem
# Register your models here.

class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0

@admin.register(TaggedItem)
class AdminTaggedItem(admin.ModelAdmin):
    list_display = ['tag','content_type','object_id','content_object']
    readonly_fields = ['content_object']