from django import template

register = template.Library()

from group.models import Group

@register.inclusion_tag('tags/group_list.html', takes_context=True)
def group_list(context):
    parent = context['request'].site.root_page
    groups = Group.objects.descendant_of(parent)

    return {
        'groups': groups
    }
