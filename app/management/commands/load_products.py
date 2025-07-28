from django.core.management.base import BaseCommand
from django.core.management import call_command
from app.models import Product  # Replace with your actual model

class Command(BaseCommand):
    help = 'Load initial product and size data (only if not already loaded)'

    def handle(self, *args, **kwargs):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING('Products already exist — skipping loaddata.'))
            return
        try:
            call_command('loaddata', 'products.json')
            self.stdout.write(self.style.SUCCESS('Successfully loaded product data!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading data: {e}'))
