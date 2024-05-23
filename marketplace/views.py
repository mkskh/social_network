from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .cart import Cart


# Create your views here.

def category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
        categories = Category.objects.all()  
        return render(request, 'marketplace/category.html', {'products': products, 'category': category, 'categories': categories})
    except Category.DoesNotExist:
        messages.success(request, "That category doesn't exist!")
        return redirect('marketplace_page')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'marketplace/product.html', {'product':product})


def marketplace_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'marketplace/marketplace.html', {'categories': categories, 'products': products})

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
    cart_products = cart.get_prods
    quantities = cart.get_quants
    return render (request, "marketplace/cart_summary.html", {"cart_products":cart_products, "quantities":quantities})


def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty', 1)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=int(product_qty))
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('marketplace:marketplace_page')))
    else:
        return redirect('marketplace:marketplace_page')


def cart_delete(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('marketplace:cart_summary')