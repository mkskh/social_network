from django.test import TestCase

# Create your tests here.

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user import views

class TestUrls(SimpleTestCase):

    def test_create_album_url(self):
        url = reverse('create_album', args=[1])
        self.assertEqual(resolve(url).func, views.create_album)

    def test_album_list_url(self):
        url = reverse('album_list', args=[1])
        self.assertEqual(resolve(url).func, views.album_list)

    def test_edit_album_url(self):
        url = reverse('edit_album', args=[1, 1])
        self.assertEqual(resolve(url).func, views.edit_album)

    def test_delete_album_url(self):
        url = reverse('delete_album', args=[1, 1])
        self.assertEqual(resolve(url).func, views.delete_album)

    def test_create_photo_url(self):
        url = reverse('create_photo', args=[1, 1])
        self.assertEqual(resolve(url).func, views.create_photo)

    def test_photo_list_url(self):
        url = reverse('photo_list', args=[1, 1])
        self.assertEqual(resolve(url).func, views.photo_list)

    def test_delete_photo_url(self):
        url = reverse('delete_photo', args=[1, 1, 1])
        self.assertEqual(resolve(url).func, views.delete_photo)

    def test_edit_photo_url(self):
        url = reverse('edit_photo', args=[1, 1, 1])
        self.assertEqual(resolve(url).func, views.edit_photo)

    def test_photo_gallery_url(self):
        url = reverse('photo_gallery', args=[1, 1, 1])
        self.assertEqual(resolve(url).func, views.photo_gallery)