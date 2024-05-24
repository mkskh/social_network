from django.test import TestCase
from django.contrib.auth.models import User
from marketplace.models import Category, Customer, Product, Order


class OrderModelTest(TestCase):
    def setUp(self):
        # Create a category
        self.category = Category.objects.create(name='Test Category')

        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            category=self.category,
            image='path/to/image.jpg',
            seller=self.user
        )

        # Create a customer
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            email='john@example.com',
            password='password'
        )

    def test_order_creation(self):
        # Create an order
        order = Order.objects.create(
            product=self.product,
            customer=self.customer,
            quantity=2,
            address='123 Test St',
            phone='1234567890',
            status=True
        )

        # Verify that the order was created successfully
        self.assertIsNotNone(order)
