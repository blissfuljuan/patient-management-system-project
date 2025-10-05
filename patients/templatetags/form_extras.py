from django import template
register = template.Library()

@register.filter
def add_class(field, css):
    existing = field.field.widget.attrs.get('class', "")
    merged = f"{existing} {css}".strip()
    return field.as_widget(attrs={"class": merged})
