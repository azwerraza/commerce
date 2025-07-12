# your_app/templatetags/cart_tag.py

from django import template
from commerce.cart import Cart


register = template.Library()

@register.simple_tag(takes_context=True)
def cart_item_count(context):
    request = context['request']
    cart = Cart(request)
    return len(cart)

@register.simple_tag(takes_context=True)
def cart_total_price(context):
    request = context['request']
    cart = Cart(request)
    return cart.get_total_price()
