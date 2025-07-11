# app/migrations/0018_emergency_fix.py
from django.db import migrations, models  # Added missing 'models' import


def fix_invalid_products(apps, schema_editor):
    Order = apps.get_model('app', 'Order')
    Product = apps.get_model('app', 'Product')

    for order in Order.objects.all():
        try:
            # If product is a ForeignKey, get its name
            if hasattr(order, 'product_id'):
                product_name = order.product.name if order.product else ''
                order.product_str = product_name
            # If product is already a string
            else:
                order.product_str = order.product
            order.save()
        except Exception as e:
            print(f"Error processing order {order.id}: {e}")
            order.product_str = ""  # Set empty string as fallback
            order.save()


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0017_convert_product_to_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_str',
            field=models.CharField(max_length=1000, blank=True, default=''),
        ),
        migrations.RunPython(fix_invalid_products),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='product_str',
            new_name='product',
        ),
    ]