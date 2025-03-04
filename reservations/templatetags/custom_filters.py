from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the given value with the argument"""
    try:
        return float(value) * int(arg)
    except (ValueError, TypeError):
        return 0  # Return 0 if invalid values are encountered
