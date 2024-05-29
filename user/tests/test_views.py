from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import Album, Photo, UserProfile

class AlbumViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.album = Album.objects.create(profile=self.user_profile, title='Test Album')
        self.client.login(username='testuser', password='12345')

    def test_create_album_view(self):
        response = self.client.post(reverse('create_album', args=[self.user.id]), {'title': 'New Album'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        self.assertEqual(Album.objects.count(), 2)  # One existing and one new album

    def test_album_list_view(self):
        response = self.client.get(reverse('album_list', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Album')

    def test_edit_album_view(self):
        response = self.client.post(reverse('edit_album', args=[self.user.id, self.album.id]), {'title': 'Updated Album'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful update
        self.album.refresh_from_db()
        self.assertEqual(self.album.title, 'Updated Album')

    def test_delete_album_view(self):
        response = self.client.post(reverse('delete_album', args=[self.user.id, self.album.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
        self.assertEqual(Album.objects.count(), 0)

class PhotoViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.album = Album.objects.create(profile=self.user_profile, title='Test Album')
        self.photo = Photo.objects.create(album=self.album, description='Test Photo')
        self.client.login(username='testuser', password='12345')

    def test_create_photo_view(self):
        with open('path/to/test_image.jpg', 'rb') as img:
            response = self.client.post(reverse('create_photo', args=[self.album.id, self.user.id]), {'image': img, 'description': 'New Photo'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        self.assertEqual(Photo.objects.count(), 2)  # One existing and one new photo

    def test_photo_list_view(self):
        response = self.client.get(reverse('photo_list', args=[self.user.id, self.album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Photo')

    def test_delete_photo_view(self):
        response = self.client.post(reverse('delete_photo', args=[self.user.id, self.album.id, self.photo.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
        self.assertEqual(Photo.objects.count(), 0)