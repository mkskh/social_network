from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from user.models import Album, Photo, UserProfile

class AlbumModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.album = Album.objects.create(profile=self.user_profile, title='Test Album')

    def test_album_creation(self):
        self.assertTrue(isinstance(self.album, Album))
        self.assertEqual(self.album.__str__(), 'Test Album by testuser')

class PhotoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.album = Album.objects.create(profile=self.user_profile, title='Test Album')
        self.photo = Photo.objects.create(album=self.album, description='Test Photo')

    def test_photo_creation(self):
        self.assertTrue(isinstance(self.photo, Photo))
        self.assertEqual(self.photo.__str__(), f'Photo {self.photo.id} in Test Album by testuser')