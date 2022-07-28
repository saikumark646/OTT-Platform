from django.urls import path
from .views import TaggedItemList,TaggedItemDetail

app_name = 'tags'

urlpatterns = [
    path('',TaggedItemList.as_view()),
    path('<slug:tag>/',TaggedItemDetail.as_view())
]
