from django import template

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    """
    Formats a numeric price into human-readable Uzbek format with thousand spaces.
    e.g. 850000000 -> 850 000 000
         138000000 -> 138 000 000
         2500000 -> 2 500 000
    """
    if value is None or value == '':
        return ''
    try:
        val = int(round(float(value)))
        return f"{val:,}".replace(",", " ")
    except (ValueError, TypeError):
        return str(value)
