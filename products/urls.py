from django.urls import path
from . import views

urlpatterns = [
    # Product list page
    path('', views.product_list, name='product_list'),

    # Product detail page
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Products by category
    path('category/<str:category>/', views.products_by_category, name='products_by_category'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
]
