from django.test import SimpleTestCase
from feed.forms import PublishPostForm, LeaveCommentForm


class TestForms(SimpleTestCase):

    def test_publish_post_form(self):

        form = PublishPostForm(data={
            'text': 'Test'
        })

        self.assertTrue(form.is_valid)

    
    def test_leave_comment_form(self):

        form = LeaveCommentForm(data={
            'text': 'Test Comment'
        })

        self.assertTrue(form.is_valid)



# python manage.py test feed.tests.test_forms