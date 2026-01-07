from django.urls import path
from .views import create_order, order_list, order_detail

urlpatterns = [
    path("create/", create_order, name="create_order"),
    path("", order_list, name="order_list"),
    path("<int:order_id>/", order_detail, name="order_detail"),
]
