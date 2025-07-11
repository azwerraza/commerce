# app/migrations/0017_convert_product_to_fk.py
from django.db import migrations, models
import django.db.models.deletion


def convert_product_to_foreignkey(apps, schema_editor):
    Order = apps.get_model('app', 'Order')
    Product = apps.get_model('app', 'Product')

    # Temporary field to store the relationship
    for order in Order.objects.all():
        # Get or create a Product based on the name
        product, created = Product.objects.get_or_create(
            name=order.product,  # Assuming Product has a 'name' field
            defaults={
                'price': order.price,  # Set default price from order
                # Add other required Product fields here
            }
        )
        order.product_temp = product  # Store in temporary field
        order.save()


def reverse_conversion(apps, schema_editor):
    Order = apps.get_model('app', 'Order')
    for order in Order.objects.all():
        if hasattr(order, 'product_temp'):
            order.product = order.product_temp.name
            order.save()


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0016_news_alter_order_date_alter_order_image_and_more'),
    ]

    operations = [
        # Add temporary foreign key field
        migrations.AddField(
            model_name='order',
            name='product_temp',
            field=models.ForeignKey(
                'Product',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='temp_orders'
            ),
        ),

        # Run data migration
        migrations.RunPython(
            convert_product_to_foreignkey,
            reverse_conversion
        ),

        # Remove old char field
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),

        # Rename new field to original name
        migrations.RenameField(
            model_name='order',
            old_name='product_temp',
            new_name='product',
        ),
    ]