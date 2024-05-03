from django.shortcuts import render
from .models import Product

# Create your views here.

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'marketplace/product.html', {'product':product})

def marketplace_page(request):
    products = Product.objects.all()
    return render(request, 'marketplace/marketplace.html', {'products':products})


def about(request):
    return render(request, 'marketplace/about.html')