from django.urls import path
from .views import CategoryListView,CategoryDetailView

app_name = 'categories'

urlpatterns = [
    path('',CategoryListView.as_view()),
    path('<slug:slug>/',CategoryDetailView.as_view() )
]
