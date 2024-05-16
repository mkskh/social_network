from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)  # Corrected from product_id to product.id
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def remove(self, product_id):
        # Remove the specified product from the cart
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]
            self.session.modified = True






    # def update(self, product, quantity):
    #     product_id = str(product.id)  # Assuming 'product' is the actual product object
    #     product_qty = int(quantity)

    #     if product_id in self.cart:
    #         self.cart[product_id] = product_qty
    #         self.session.modified = True
    #         return product_qty  # Return only the updated quantity
    #     else:
    #         # Handle case where product is not found in the cart
    #         raise KeyError("Product not found in the cart")

