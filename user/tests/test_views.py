from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import Album, Photo, UserProfile
from user.views import create_album

# Create your tests here.
class AlbumViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = self.user.userprofile
        self.client.login(username='testuser', password='12345')
        self.album = Album.objects.create(profile=self.user_profile, title='Test Album')

        # creation of multiple for the album_list view
        self.album1 = Album.objects.create(profile=self.user_profile, title='Album 1', description='Description 1')
        self.album2 = Album.objects.create(profile=self.user_profile, title='Album 2', description='Description 2')


    def test_create_album_get(self):
        # Test GET request to load the album creation form
        url = reverse('user:create_album', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/create_album.html')

    def test_create_album_post(self):
        # Test POST request to create an album
        url = reverse('user:create_album', kwargs={'user_id': self.user.id})
        data = {
            'title': 'Test Album',
            'description': 'Test Description',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)



    def test_album_list_view(self):
        url = reverse('user:album_list', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/album_list.html')

        # Check that the response contains the albums
        self.assertContains(response, 'Album 1')
        self.assertContains(response, 'Album 2')

        # Check that the context contains the correct albums and is_owner flag
        self.assertEqual(list(response.context['albums']), [self.album, self.album1, self.album2])
        self.assertTrue(response.context['is_owner'])