from django import template
from decimal import Decimal, ROUND_HALF_UP

register = template.Library()

@register.filter
def currency_br(value):
    """Formata Decimal/float para string com vírgula e 2 casas, ex: 200,89"""
    if value is None:
        return "0,00"
    try:
        v = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except:
        try:
            v = Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except:
            return "0,00"
    s = f"{v:.2f}"
    return s.replace('.', ',')
