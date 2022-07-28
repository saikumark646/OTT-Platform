from django.test import TestCase
from .models import Video
# Create your tests here.

class VideoModelTestCase(TestCase):
    def setup(self):
        Video.objects.create(title ='this is a best video')
        
    def test_valid_title(self):
        title = 'this is a best video!!!'
        qs = Video.objects.filter(title = title)
        self.assertTrue(qs.exists())
    
    def test_created_count(self):
        qs = Video.objects.all()
        print(qs)
        self.assertEqual(qs.count(),1)