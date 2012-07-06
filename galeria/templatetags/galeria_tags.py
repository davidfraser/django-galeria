from django import template

from galeria.models import Picture


register = template.Library()


class RandomPictureListNode(template.Node):
    def __init__(self, num, var_name):
        self.num = int(num)
        self.var_name = var_name

    def render(self, context):
        random_pictures = Picture.objects.public().order_by('?')
        context[self.var_name] = list(random_pictures[:self.num])
        return ''


def do_get_random_pictures(parser, token):
    """
    Gets N random pictures and populates the template context with a variable
    containing that value, whose name is defined by the 'as' clause.

    Syntax::

        {% get_random_pictures [num] as [var_name] %}

    Example::

        {% get_random_pictures 6 as random_picture_list %}

    """
    bits = token.contents.split()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
        return RandomPictureListNode(num=bits[1], var_name=bits[3])
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]


register.tag('get_random_pictures', do_get_random_pictures)
