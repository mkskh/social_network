from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from marketplace.models import Product, Category
from marketplace.forms import ProductForm

class MarketplaceTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(name='TestProduct', description='TestDescription', price=10, category=self.category, seller=self.user)

    def test_category_view(self):
        response = self.client.get(reverse('marketplace:category', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_product_view(self):
        response = self.client.get(reverse('marketplace:product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_marketplace_page_view(self):
        response = self.client.get(reverse('marketplace:marketplace_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.product.name)

    def test_add_product_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('marketplace:add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ProductForm)
        form_data = {'name': 'NewProduct', 'description': 'NewDescription', 'price': 20, 'category': self.category.id}
        response = self.client.post(reverse('marketplace:add_product'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='NewProduct').exists())

    def test_delete_product_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('marketplace:delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_added_products_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('marketplace:added_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_cart_summary_view(self):
        response = self.client.get(reverse('marketplace:cart_summary'))
        self.assertEqual(response.status_code, 200)

    def test_cart_add_view(self):
        form_data = {'product_id': self.product.id, 'product_qty': 1}
        response = self.client.post(reverse('marketplace:cart_add'), form_data)
        self.assertEqual(response.status_code, 302)

    def test_cart_delete_view(self):
        form_data = {'product_id': self.product.id}
        response = self.client.post(reverse('marketplace:cart_delete'), form_data)
        self.assertEqual(response.status_code, 302)
