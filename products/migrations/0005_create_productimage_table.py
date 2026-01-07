from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_slug'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS products_productimage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image VARCHAR(100) NOT NULL,
                alt VARCHAR(250),
                product_id INTEGER NOT NULL REFERENCES products_product(id) DEFERRABLE INITIALLY DEFERRED
            );
            """
        ),
    ]
