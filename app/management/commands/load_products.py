from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Load initial product data from products_clean.json"

    def handle(self, *args, **kwargs):
        try:
            call_command('loaddata', 'products_clean.json')
            self.stdout.write(self.style.SUCCESS('✅ Successfully loaded product data!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Error loading data: {e}'))
