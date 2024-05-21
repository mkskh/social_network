from django.test import TestCase
from rest_framework.test import APIRequestFactory
from.views import BulkCreateUsers
from.models import ApiUser










class BulkCreateUsersTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BulkCreateUsers.as_view()

    def test_create_with_invalid_data_type(self):
        # Test with a non-list data type
        request = self.factory.post('/api/users/bulk/', data={'name': 'John Doe', 'email': 'johndoe@example.com'})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request status code

    def test_create_with_empty_list(self):
        # Test with an empty list
        request = self.factory.post('/api/users/bulk/', data=[])
        response = self.view(request)
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request status code

    def test_create_with_single_dict(self):
        # Test with a single dictionary
        request = self.factory.post('/api/users/bulk/', data={'name': 'John Doe', 'email': 'johndoe@example.com'})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request status code

    def test_create_with_incomplete_dict(self):
        # Test with a dictionary missing required fields
        request = self.factory.post('/api/users/bulk/', data=[{'name': 'John Doe'}, {'email': 'janedoe@example.com'}])
        response = self.view(request)
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request status code

    def test_create_with_invalid_dict(self):
        # Test with a dictionary containing invalid data
        request = self.factory.post('/api/users/bulk/', data=[{'name': 'John Doe', 'email': 'johndoe'}, {'name': 'Jane Doe', 'email': 'janedoe@example.com'}])
        response = self.view(request)
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request status code