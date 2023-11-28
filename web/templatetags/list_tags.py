from django import template

register = template.Library()

@register.filter
def rows(value, row_length):
    """
    Разбивает список на подсписки указанной длины.
    """
    row_length = int(row_length)
    return [value[i:i+row_length] for i in range(0, len(value), row_length)]