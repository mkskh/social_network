from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .cart import Cart
from decimal import Decimal

# Create your views here.

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
    product = Product.objects.get(id=pk)
    return render(request, 'marketplace/product.html', {'product':product})


def marketplace_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    
    
    if request.method == 'GET':
        product_name = request.GET.get('product_name')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')

        
        if price_min:
            try:
                price_min = Decimal(price_min)
            except ValueError:
                price_min = None
        if price_max:
            try:
                price_max = Decimal(price_max)
            except ValueError:
                price_max = None

        
        filters = {}
        if product_name:
            filters['name__icontains'] = product_name
        if price_min is not None:
            filters['price__gte'] = price_min
        if price_max is not None:
            filters['price__lte'] = price_max
        
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



def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty', 1)
        selected_quantity = request.POST.get('selected_quantity', 1)  
        try:
            quantity = int(selected_quantity)
        except ValueError:
            
            quantity = 1 
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity)
        
        
        request.session[f'cart_quantity_{product_id}'] = 1
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('marketplace:marketplace_page')))
    else:
        return redirect('marketplace:marketplace_page')
    

def cart_update(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty', 1))
        product = get_object_or_404(Product, id=product_id)
        cart.update(product=product, quantity=product_qty)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def cart_delete(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('marketplace:cart_summary')


def payment_view(request):
    return render(request, 'marketplace/payment.html')