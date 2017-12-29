# !usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'xinlan'
from django import template
from django.utils.timezone import datetime, timedelta
register = template.Library()


@register.simple_tag
def record_is_need_review(record):
    """

    :param record:
    :return:
    """
    config = {
        0: timedelta(days=1),
        1: timedelta(days=3),
        2: timedelta(days=7),
        3: timedelta(days=15),
        4: timedelta(days=30),
        5: timedelta(days=90),
        6: timedelta(days=180)
    }
    tr_str = "<tr>%s</tr>"

    if datetime.now().date()-config[record.type] >= record.c_time.date():
        return record


@register.simple_tag
def get_review_str(record):
    """返回复习按钮文本"""
    config = {
        0: '隔一天复习',
        1: '隔三天复习',
        2: '隔7天复习',
        3: '隔15天复习',
        4: '隔30天复习',
        5: '隔90天复习',
        6: '隔180天复习',
    }
    return config[record.type]