from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from .models import Product


# ======= Product list (home) =======
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


# ======= Product detail =======
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})


# ======= CART (session-based) =======
def cart_view(request):
    session_cart = request.session.get("cart", {})
    cart_items = []
    total = Decimal("0.0")

    if session_cart:
        product_ids = [int(pid) for pid in session_cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        products_map = {p.id: p for p in products}

        for pid_str, qty in session_cart.items():
            try:
                pid = int(pid_str)
            except ValueError:
                continue
            product = products_map.get(pid)
            if not product:
                continue
            quantity = int(qty)
            subtotal = Decimal(product.price) * quantity
            total += subtotal
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

    context = {
        "cart_items": cart_items,
        "total": total,
    }
    return render(request, "products/cart.html", context)


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)
    if pid in cart:
        cart[pid] += 1
    else:
        cart[pid] = 1
    request.session["cart"] = cart
    return redirect("product_list")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    request.session["cart"] = cart
    return redirect("cart")


def increase_quantity(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)
    if pid in cart:
        cart[pid] += 1
    request.session["cart"] = cart
    return redirect("cart")


def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)
    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            del cart[pid]
    request.session["cart"] = cart
    return redirect("cart")


# ======= Products by category view =======
def products_by_category(request, category):
    category_map = {
        "men": "مردانه",
        "women": "زنانه",
        "unisex": "یونیسکس"
    }

    if category not in category_map:
        # optionally return a 404 page; here we render a simple 404 template if exists
        return render(request, "404.html", status=404)

    products = Product.objects.filter(category=category)

    return render(request, "products/products_by_category.html", {
        "products": products,
        "category_name": category_map[category]
    })
