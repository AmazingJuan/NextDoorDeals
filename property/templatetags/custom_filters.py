from django import template

register = template.Library()

@register.filter
def getTypeID(queryset, id):
    return queryset.filter(id=id).first().name
