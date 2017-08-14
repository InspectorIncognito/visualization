# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def columns(md, sm, xs, body):

    content = u"""
        <div class='col-md-{} col-sm-{} col-xs-{}'>
        {}
        </div>
    """

    return format_html(content, md, sm, xs, body)