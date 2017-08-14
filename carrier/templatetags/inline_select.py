# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def inline_select(label, input_id, optionList):

    options = []
    for option in optionList:
        option = u"<option>{}</option>".format(option)
        options.append(option)

    content = u"""
        <div class="form-group">
            <label for="{1}">{0}</label>
            <select class="select2_multiple form-control" id="{1}" multiple="multiple">
                """ + "".join(options) + """
            </select>
        </div>
    """

    return format_html(content, label, input_id)