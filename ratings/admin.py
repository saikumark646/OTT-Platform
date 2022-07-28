from django.contrib import admin
from .models import Rating
# Register your models here.
@admin.register(Rating)
class AdminRating(admin.ModelAdmin):
    list_display = ['value','content_type','object_id','content_object']
    readonly_fields = ['content_object']