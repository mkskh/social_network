from django.urls import path
from . import views
from .views import add_product

app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace_page, name='marketplace_page'),
    path('product/<int:pk>/', views.product, name='product'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('add_product/', views.add_product, name='add_product'),
    path('added_products/', views.added_products, name='added_products'),
    path('cart_summary/', views.cart_summary, name='cart_summary'),
    path('add/', views.cart_add, name='cart_add'),
    path('cart_delete/', views.cart_delete, name='cart_delete'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]