from django import template

register = template.Library()

@register.filter
def rental_rate(base_price, days):
    return round((base_price / 3) * int(days))
