from django.urls import path
from .views import home, product_detail, about, contact

urlpatterns = [
    path('', home, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]
