from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from products.models import Product
from .models import Order, OrderItem

@login_required
def create_order(request):
    cart = request.session.get("cart", {})

    if not cart:
        return render(request, "orders/empty_cart.html")

    total = Decimal("0")
    items = []

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = int(quantity)

        unit_price = Decimal(product.price)     # قیمت واحد
        subtotal = unit_price * quantity        # جمع هر محصول

        total += subtotal

        items.append({
            "product": product,
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": subtotal
        })

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            quantity=item["quantity"],
            price=item["unit_price"]
        )

    request.session["cart"] = {}

    return render(request, "orders/order_success.html", {"order": order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})
