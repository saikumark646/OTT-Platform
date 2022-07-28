from django.contrib import admin
from .models import Categories
# Register your models here.
@admin.register(Categories)
class AdminCategories(admin.ModelAdmin):
    list_display = ['title','slug','active']