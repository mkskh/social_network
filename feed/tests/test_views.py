from django.test import TestCase, Client
from django.urls import reverse
from feed.models import Post, Like, Comment
import json
from django.contrib.auth.models import User
from user.models import UserProfile


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.news_feed_url = reverse('feed:news_feed')

        # for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)

        # Log in the test client
        self.client.login(username='testuser', password='testpassword')

        self.post = Post.objects.create(profile=self.user_profile, text='Test')

        self.like_unlike_post_url = reverse('feed:like_unlike_post')

    def test_news_feed_GET(self):
        response = self.client.get(self.news_feed_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed/news_feed.html')


    def test_news_feed_POST_add_comment(self):

        Comment.objects.create(
            profile=self.user_profile, 
            text='Test comment', 
            post=self.post
        )

        response = self.client.post(self.news_feed_url, {
            'text': 'Test comment',
            'post_id': self.post.id 
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('feed:news_feed'))


    def test_like_unlike_post_POST(self):

        initial_likes_count = self.post.num_likes()

        Like.objects.create(
            profile=self.user_profile, 
            post=self.post,
            value='Like'
        )

        response = self.client.post(self.like_unlike_post_url, {
            'value': 'Like',
            'post_id': self.post.id
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.num_likes(), initial_likes_count + 1)




# python manage.py test feed.tests.test_views