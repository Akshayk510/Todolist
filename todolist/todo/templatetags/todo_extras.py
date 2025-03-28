from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        # Convert to integers if possible
        value_int = int(value) if value is not None else 0
        arg_int = int(arg) if arg is not None else 0
        return value_int - arg_int
    except (ValueError, TypeError):
        try:
            # If not integers, try direct subtraction
            if value is None:
                value = 0
            if arg is None:
                arg = 0
            return value - arg
        except Exception:
            # Return 0 if all else fails
            return 0

@register.filter
def completed_count(tasks):
    """Count the number of completed tasks in a queryset."""
    if tasks is None or not hasattr(tasks, '__iter__'):
        return 0
    try:
        return sum(1 for task in tasks if getattr(task, 'completed', False))
    except (TypeError, AttributeError):
        return 0