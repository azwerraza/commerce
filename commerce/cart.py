from decimal import Decimal
from django.conf import settings
from app.models import Product, Size

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size=None, quantity=1, update_quantity=False, rental_days=None, rental_price=None):
        product_id = str(product.id)
        size_id = str(size.id) if size else ''

        # 🧠 Include rental days in cart key for uniqueness
        rental_key = f"_rental_{rental_days}" if rental_days else ""
        cart_key = f"{product_id}_{size_id}{rental_key}"

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'quantity': 0,
                'price': str(rental_price if rental_price else product.price),
                'size_id': size_id,
                'size_name': size.name if size else 'No size',
                'rental_days': rental_days,
                'is_rental': bool(rental_days)
            }

        if update_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity

        self.save()

    def decrement(self, product, size=None, rental_days=None):
        product_id = str(product.id)
        size_id = str(size.id) if size else ''
        rental_key = f"_rental_{rental_days}" if rental_days else ""
        cart_key = f"{product_id}_{size_id}{rental_key}"

        if cart_key in self.cart:
            if self.cart[cart_key]['quantity'] > 1:
                self.cart[cart_key]['quantity'] -= 1
            else:
                del self.cart[cart_key]
            self.save()

    def remove(self, product, size=None, rental_days=None):
        product_id = str(product.id)
        size_id = str(size.id) if size else ''

        for key in list(self.cart.keys()):
            if key.startswith(f"{product_id}_{size_id}"):
                if rental_days:
                    if f"_rental_{rental_days}" in key:
                        del self.cart[key]
                        break
                else:
                    # No rental_days → likely normal product or rental item without days supplied
                    if "_rental_" not in key:
                        del self.cart[key]
                        break

        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = {key.split('_')[0] for key in self.cart.keys()}
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            for key, item in self.cart.items():
                if key.startswith(f"{product.id}_"):
                    yield {
                        'product': product,
                        'quantity': item['quantity'],
                        'price': item['price'],
                        'total_price': Decimal(item['price']) * item['quantity'],
                        'size_id': item['size_id'],
                        'size_name': item['size_name'],
                        'rental_days': item.get('rental_days'),
                        'is_rental': item.get('is_rental', False),
                        'cart_key': key
                    }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
