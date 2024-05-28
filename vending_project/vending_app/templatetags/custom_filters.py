from django import template
# 숫자를 3자리마다 쉼표로 구분하여 표시하는 필터

register = template.Library()

@register.filter
def intcomma(value):
    return f"{value:,}"