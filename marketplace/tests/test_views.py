from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from marketplace.models import Product, Category


class CategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.category = Category.objects.create(name='Test Category')

    def test_category_view(self):
        response = self.client.get(reverse('marketplace:category', args=(self.category.id,)))
        self.assertEqual(response.status_code, 200)

    def test_invalid_category_view(self):
        response = self.client.get(reverse('marketplace:category', args=(1000,)))  # Invalid category ID
        self.assertEqual(response.status_code, 302)  # Redirects to marketplace_page


class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=100.00, category=self.category)

    def test_product_view(self):
        response = self.client.get(reverse('marketplace:product', args=(self.product.id,)))
        self.assertEqual(response.status_code, 200)


class MarketplacePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_marketplace_page_view(self):
        response = self.client.get(reverse('marketplace:marketplace_page'))
        self.assertEqual(response.status_code, 200)


class AddProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_add_product_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('marketplace:add_product'), {'name': 'Test Product', 'price': 100.00})
        self.assertRedirects(response, reverse('marketplace:marketplace_page'))  # Check for redirection
