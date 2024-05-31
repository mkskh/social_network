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
    path('cart_update/', views.cart_update, name='cart_update'),
    path('cart_delete/', views.cart_delete, name='cart_delete'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('payment_view/', views.payment_view, name='payment'),
     path('bn_payment_view/', views.bn_payment_view, name='bn_payment_view'),
    path('shipping/', views.shipping_form_view, name='shipping_form'),
    path('bn_shipping_form/', views.bn_shipping_form_view, name='bn_shipping_form_view'),
    path('buy_now/', views.buy_now, name='buy_now'),
    path('success/', views.success_page, name='success_page'),
]