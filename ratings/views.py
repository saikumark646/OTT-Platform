from django.http import HttpResponseNotAllowed, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from ratings.forms import RatingForm
from ratings.models import Rating
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def rate_object_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            rating = cd.get('rating')
            object_id = cd.get('object_id')
            content_type_id = cd.get('content_type_id')
            c_type = ContentType.objects.get_for_id(content_type_id)
            obj = Rating.objects.create(
                content_type = c_type,
                object_id = object_id,
                value = rating,
                user = request.user
            )
            next_path = cd.get('next')  #detail view
            return HttpResponseRedirect(next_path)
    return HttpResponseRedirect('/')
