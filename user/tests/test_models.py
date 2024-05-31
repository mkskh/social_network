from django.test import TestCase
from django.contrib.auth.models import User
from user.models import Album, Photo, UserProfile

from datetime import datetime
from django.db.models.signals import post_save
from user.signals import create_profile, save_profile
# Create your tests here.




class UserProfileTestCase(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_user_profile_creation(self):
        # Check if UserProfile instance is created when a User is created
        user_profile = self.user.userprofile
        self.assertIsInstance(user_profile, UserProfile)
        self.assertEqual(user_profile.user, self.user)

    def test_edit_profile(self):
        # Retrieve the UserProfile instance
        user_profile = self.user.userprofile

        # check the values of the Newlx UserProfile created. should equal to None.
        self.assertEqual(user_profile.date_of_birth, None)
        self.assertEqual(user_profile.gender, None)
        self.assertEqual(user_profile.phone, None)
        self.assertEqual(user_profile.location, None)
        self.assertEqual(user_profile.description, None)

        # Edit profile fields
        user_profile.date_of_birth = '1990-04-28'
        user_profile.gender = 'MALE'
        user_profile.phone = '1234567890'
        user_profile.location = 'Test City'
        user_profile.description = 'Updated description'
        # Save the changes
        user_profile.save()

        # Reload the UserProfile instance from the database
        user_profile.refresh_from_db()
        # Assertions
        self.assertEqual(user_profile.date_of_birth.strftime('%Y-%m-%d'), '1990-04-28')
        self.assertEqual(user_profile.gender, 'MALE')
        self.assertEqual(user_profile.phone, '1234567890')
        self.assertEqual(user_profile.location, 'Test City')
        self.assertEqual(user_profile.description, 'Updated description')


    def tearDown(self):
        self.user.delete()




class TestAlbumAndPhotoModel(TestCase):

    @classmethod
    def setUp(cls):
        # Create a user and user profile
        cls.user = User.objects.create(username='testuser', password='testP123!')
        cls.user_profile, _ = UserProfile.objects.get_or_create(user=cls.user)
        # Create an album
        cls.album = Album.objects.create(profile=cls.user_profile, title='Test Album', description='Test Description')


    def test_album_creation(self):
        
        # Assertions
        self.assertEqual(self.album.title, 'Test Album')
        self.assertEqual(self.album.description, 'Test Description')
        self.assertEqual(self.album.profile.user.username, 'testuser')
        self.assertTrue(isinstance(self.album.created_at, datetime))
        self.assertTrue(isinstance(self.album.updated_at, datetime))


    def test_photo_creation(self):
        # Create a photo
        self.photo = Photo.objects.create(album=self.album, description='Test Photo Description', image='test.jpg')

        # check the photo is created and belong to the corresponding album
        self.assertEqual(self.photo.description, 'Test Photo Description')
        self.assertIsInstance(self.photo.album, Album) 
        self.assertEqual(self.photo.album.title, 'Test Album')
        self.assertTrue(isinstance(self.photo.created_at, datetime))



