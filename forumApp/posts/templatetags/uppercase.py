from django import template
from django.template import Node

register = template.Library()


class UppercaseNode(Node):
    def __init__(self, nodelist):
        # content between custom opening and closing tags
        self.nodelist = nodelist

    def render(self, context):
        # render content between tags using the current context
        output = self.nodelist.render(context)
        # convert rendered content to uppercase before returning
        return output.upper()


# registering the 'uppercase' template tag
@register.tag(name='uppercase')
def do_uppercase(parser, token):

    # parse all between {% uppercase %} and {% enduppercase %}
    nodelist = parser.parse(('enduppercase',))

    # remove 'enduppercase' token from the parsing Q
    parser.delete_first_token()

    # returns an instance of the custom uppercaseNode with the parsed nodelist
    return UppercaseNode(nodelist)
