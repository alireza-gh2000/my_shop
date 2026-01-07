from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Products
    path('', include('products.urls')),
    path('shop/', include('products.urls')),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # Orders
    path('orders/', include('orders.urls')),

    # about/contact
    path('shop/', include('shop.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
