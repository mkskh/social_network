from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, Customer, ShippingAddress
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ShippingForm, bn_ShippingForm
from .cart import Cart
from decimal import Decimal, InvalidOperation


def category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
        categories = Category.objects.all()  
        return render(request, 'marketplace/category.html', {'products': products, 'category': category, 'categories': categories})
    except Category.DoesNotExist:
        messages.success(request, "That category doesn't exist!")
        return redirect('marketplace:marketplace_page')


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'marketplace/product.html', {'product': product})


@login_required
def marketplace_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    
    
    if request.method == 'GET':
        product_name = request.GET.get('product_name')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')

        
        filters = {}

        if product_name:
            filters['name__icontains'] = product_name

        try:
            if price_min:
                filters['price__gte'] = Decimal(price_min)
            if price_max:
                filters['price__lte'] = Decimal(price_max)
        except InvalidOperation:
            pass

        if filters:
            products = products.filter(**filters)
    
    return render(request, 'marketplace/marketplace.html', {
        'categories': categories,
        'products': products,
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.seller = request.user
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('marketplace:marketplace_page')  
        else:
            messages.error(request, "Error adding product. Please check your input.")
    else:
        form = ProductForm()
    return render(request, 'marketplace/add_product.html', {'form': form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('marketplace:added_products')


@login_required
def added_products(request):

        added_products = Product.objects.filter(seller=request.user)
        return render(request, 'marketplace/added_products.html', {'added_products': added_products})


@login_required
def cart_summary(request):
    cart = Cart(request)
    cart_items = []

    for product in cart.get_prods():
        product_id = str(product.id)
        quantity = cart.get_quants().get(product_id, 0)
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

    context = {
        'cart_products': cart_items,
        'cart': cart,
    }
    return render(request, 'marketplace/cart_summary.html', context)



@login_required
def cart_add(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        if cart.has_product(product_id):
            messages.info(request, 'Product already added to the cart.')
        else:
            cart.add(product=product, quantity=quantity)
            messages.success(request, 'Product added to the cart successfully.')
        
        return redirect('marketplace:product', pk=product_id)
    else:
        return redirect('marketplace:marketplace_page')
    
    
# @login_required
# def buy_now(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         quantity = int(request.POST.get('quantity', 1))

#         product = get_object_or_404(Product, id=product_id)

#         cart = Cart(request)
#         if not cart.has_product(product_id):
#             cart.add(product=product, quantity=quantity)
#             messages.success(request, 'Product added to the cart successfully.')
#         else:
#             messages.info(request, 'Product already in the cart.')

#         return redirect('marketplace:cart_summary')
#     else:
#         return redirect('marketplace:marketplace_page')


    


@login_required
def cart_update(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty', 1))
        product = get_object_or_404(Product, id=product_id)
        cart.update(product=product, quantity=product_qty)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def cart_delete(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('marketplace:cart_summary')



def payment_view(request):
    if request.method == 'POST':
        
        cart = Cart(request)
        total_price = cart.get_total_price()
        request.session['total_price'] = total_price
        cart.clear()
        return redirect('marketplace:success_page')

    return render(request, 'marketplace/payment.html')




@login_required
def shipping_form_view(request):
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            user = request.user
            
            customer, created = Customer.objects.get_or_create(
                email=user.email,
                defaults={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': '',
                    'password': user.password,
                }
            )
            
            shipping_address = form.save(commit=False)
            shipping_address.user = user
            shipping_address.save()

            
            return render(request, 'marketplace/payment.html', {'shipping_info': shipping_address})
    else:
        form = ShippingForm()
    return render(request, 'marketplace/shipping_form.html', {'form': form})


@login_required
def buy_now(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        request.session['buy_now_product'] = {
            'product_id': product.id,
            'quantity': quantity,
            'price': str(product.sale_price if product.is_sale else product.price),
        }

        cart = Cart(request)
        if not cart.has_product(product_id):
            # cart.add(product=product, quantity=quantity)
            messages.success(request, 'Product added to the cart successfully.')
            return redirect('marketplace:bn_shipping_form_view')
        else:
            messages.info(request, 'Product already in the cart.')

            return redirect('marketplace:cart_summary')
    else:
        return redirect('marketplace:marketplace_page')



    
    
@login_required
def bn_shipping_form_view(request):
    if request.method == 'POST':
        form = bn_ShippingForm(request.POST)
        if form.is_valid():
            user = request.user
            
            customer, created = Customer.objects.get_or_create(
                email=user.email,
                defaults={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': '',
                    'password': user.password,
                }
            )
            
            shipping_address = form.save(commit=False)
            shipping_address.user = user
            shipping_address.save()

            # Retrieve product details from the session
            buy_now_product = request.session.get('buy_now_product', None)
            if buy_now_product:
                price = buy_now_product['price']
                quantity = buy_now_product['quantity']
                total_price = price * quantity
            else:
                total_price = 0

            return render(request, 'marketplace/bn_payment.html', {
                'shipping_info': shipping_address,
                'total_price': total_price,
            })
    else:
        form = bn_ShippingForm()
    return render(request, 'marketplace/shipping_form.html', {'form': form})


# @login_required
# def bn_shipping_form_view(request):
#     if request.method == 'POST':
#         form = bn_ShippingForm(request.POST)
#         if form.is_valid():
#             user = request.user
            
#             customer, created = Customer.objects.get_or_create(
#                 email=user.email,
#                 defaults={
#                     'first_name': user.first_name,
#                     'last_name': user.last_name,
#                     'phone': '',
#                     'password': user.password,
#                 }
#             )
            
#             shipping_address = form.save(commit=False)
#             shipping_address.user = user
#             shipping_address.save()

#             card_number = request.POST.get('card_number')
#             if not card_number or len(card_number.replace(' ', '')) != 16:
#                 messages.error(request, 'Please enter a valid 16-digit card number.')
#                 return render(request, 'marketplace/bn_payment.html', {
#                     'shipping_info': shipping_address,
#                     'total_price': request.session.get('total_price', 0),
#                 })

#             # Here you would handle the payment processing logic

#             return redirect('marketplace:success_page')
#     else:
#         form = bn_ShippingForm()
#     return render(request, 'marketplace/shipping_form.html', {'form': form})





@login_required
def bn_payment_view(request):
    buy_now_product = request.session.get('buy_now_product')
    shipping_info = request.session.get('shipping_info')

    if not buy_now_product or not shipping_info:
        return redirect('marketplace:marketplace_page')

    context = {
        'product_id': buy_now_product['product_id'],
        'quantity': buy_now_product['quantity'],
        'price': buy_now_product['price'],
        'shipping_info': shipping_info,
    }

    if request.method == 'POST':
        # Handle payment processing here
        messages.success(request, 'Payment successful.')
        return redirect('marketplace:order_confirmation')

    return render(request, 'marketplace/bn_payment.html', context)





@login_required
def success_page(request):
    
    cart = Cart(request)
    cart_products = cart.get_prods()
    shipping_info = ShippingAddress.objects.filter(user=request.user).latest('id')

    cart.clear()

    context = {
        'cart_products': cart_products,
        'shipping_info': shipping_info,
    }
    return render(request, 'marketplace/success_page.html', context)