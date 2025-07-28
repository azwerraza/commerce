# export_products.py

import os
import sys
import django
from django.core.management import call_command

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')  # change if needed
django.setup()

# Dump the Product model data safely with UTF-8 encoding
with open('products.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'app.Product', stdout=f)
