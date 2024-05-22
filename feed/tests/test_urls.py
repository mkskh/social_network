from django.test import SimpleTestCase
from django.urls import resolve, reverse
from feed.views import news_feed, like_unlike_post, delete_post


class TestUrls(SimpleTestCase):

    def test_news_feed(self):
        url = reverse('feed:news_feed')
        self.assertEquals(resolve(url).func, news_feed)

    def test_like_unlike_post(self):
        url = reverse('feed:like_unlike_post')
        self.assertEquals(resolve(url).func, like_unlike_post)

    def test_delete_post(self):
        url = reverse('feed:delete_post', args=[1])
        self.assertEquals(resolve(url).func, delete_post)


# python manage.py test feed.tests.test_urls