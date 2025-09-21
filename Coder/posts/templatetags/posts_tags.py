from django import template
from ..models import Tags, Category, Reaction

register = template.Library()


@register.inclusion_tag('posts/template_tags/menu_block.html', name='menu_block', takes_context=True)
def show_menu_block(context):
    request = context.get('request')
    cats = Category.objects.order_by('?')[:5]
    tags = Tags.objects.order_by('?')[:5]

    return {
        'cat_list': cats,
        'tags_list': tags,
        'user': request.user,
        'perms': context.get('perms', request.user.get_all_permissions())
    }


@register.simple_tag
def get_pretty_reaction(reaction_count):
    count = int(reaction_count)
    if count >= 1000000:
        return f'{round(count / 1000000, 1)} млн'
    elif count >= 1000:
        return f'{round(count / 1000, 1)} тыс'
    return count