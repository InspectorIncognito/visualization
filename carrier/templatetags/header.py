# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def header(title, subtitle="", right=""):
    content = u"""
      <div class="page-title">
        <div class="title_left">
          <h3>{} <small>{}</small></h3>
        </div>
        <div class="title_right">
          {}
        </div>
      </div>
      <div class="clearfix"></div>
      <br />
    """
    return format_html(content, title, subtitle, right)