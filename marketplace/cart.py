from .models import Product

class Cart:
    CART_SESSION_ID = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.CART_SESSION_ID)
        if not cart:
            cart = self.session[self.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.session.modified = True



    def __len__(self):
        return sum(self.cart.values())

    def get_prods(self):
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        return self.cart

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def save(self):
        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] = quantity
            self.session.modified = True

    def clear(self):
        del self.session[self.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        total_price = 0
        for product_id, quantity in self.cart.items():
            product = Product.objects.get(id=product_id)
            total_price += product.price * quantity
        return total_price