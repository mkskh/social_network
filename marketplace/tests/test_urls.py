from django.test import SimpleTestCase
from django.urls import reverse, resolve
from marketplace.views import (
    marketplace_page,
    product,
    category,
    add_product,
    added_products,
    cart_summary,
    cart_add,
    cart_delete,
    delete_product,
)

class TestUrls(SimpleTestCase):
    def test_marketplace_page_url_resolves(self):
        url = reverse('marketplace:marketplace_page')
        self.assertEqual(resolve(url).func, marketplace_page)

    def test_product_url_resolves(self):
        url = reverse('marketplace:product', args=[1])  # Assuming product ID 1
        self.assertEqual(resolve(url).func, product)

    def test_category_url_resolves(self):
        url = reverse('marketplace:category', args=[1])  # Assuming category ID 1
        self.assertEqual(resolve(url).func, category)

    def test_add_product_url_resolves(self):
        url = reverse('marketplace:add_product')
        self.assertEqual(resolve(url).func, add_product)

    def test_added_products_url_resolves(self):
        url = reverse('marketplace:added_products')
        self.assertEqual(resolve(url).func, added_products)

    def test_cart_summary_url_resolves(self):
        url = reverse('marketplace:cart_summary')
        self.assertEqual(resolve(url).func, cart_summary)

    def test_cart_add_url_resolves(self):
        url = reverse('marketplace:cart_add')
        self.assertEqual(resolve(url).func, cart_add)

    def test_cart_delete_url_resolves(self):
        url = reverse('marketplace:cart_delete')
        self.assertEqual(resolve(url).func, cart_delete)

    def test_delete_product_url_resolves(self):
        url = reverse('marketplace:delete_product', args=[1])  # Assuming product ID 1
        self.assertEqual(resolve(url).func, delete_product)