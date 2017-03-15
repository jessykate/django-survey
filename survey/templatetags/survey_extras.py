# -*- coding: utf-8 -*-

from django import template

register = template.Library()


class CounterNode(template.Node):

    def __init__(self):
        self.count = 0

    def render(self, context):
        self.count += 1
        return self.count


@register.tag
def counter(parser, token):
    return CounterNode()
