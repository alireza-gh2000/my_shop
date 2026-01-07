from django.db import models

# Product categories
CATEGORY_CHOICES = [
    ('women', 'زنانه'),
    ('men', 'مردانه'),
    ('unisex', 'یونیسکس'),
]

# Main product model
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='unisex')

    def __str__(self):
        return self.title


# Product image gallery
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")
    alt = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.product.title} - image #{self.id}"


# Product features
class Feature(models.Model):
    product = models.ForeignKey(Product, related_name="features", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.value}"
