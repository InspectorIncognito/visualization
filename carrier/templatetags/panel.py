# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def panel(title_icon, title, body, title_id="", show_collapse=False):

    collapse = u"""
        <ul class="nav navbar-right panel_toolbox">
          <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a></li>
        </ul>
        """
    if not show_collapse:
        collapse = ""

    header = u"""
        <div class="x_title">
          <h2><i class="fa {}"></i> <span id="{}">{}</span></h2>
          """ + collapse + u"""
          <div class="clearfix"></div>
        </div>
        """

    content = u"""
        <div class="x_content">
          {}
        </div>"""
    header = header if title != "" else ""
    panel = u"<div class='x_panel'>" + header + content + u"</div>"
    return format_html(panel, title_icon, title_id, title, body)