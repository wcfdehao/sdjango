# !usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'xinlan'
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(obj, admin_class, app_name, table_name):
    """
    输出表格每行数据
    :param obj:
    :param admin_class:
    :return:
    """
    row = ""
    url = reverse('king_admin:table_obj_change', args=(app_name, table_name, obj.id))
    for column in admin_class.list_display:
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:  # choice类型
            column_data = getattr(obj, "get_%s_display" % column)()
        else:
            column_data = getattr(obj, column)
        if type(column_data).__name__ == 'datetime':
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        if row:
            row += "<td>%s</td>" % column_data
        else:
            row += "<td><a href='%s'>%s</a></td>" % (url, column_data)

    return mark_safe(row)


@register.simple_tag
def render_filter_ele(condition, admin_class, filter_conditions):
    """
    过滤条件html
    :param condition:
    :param admin_class:
    :param filter_conditions:
    :return:
    """
    field_obj = admin_class.model._meta.get_field(condition)
    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
        select_ele = """<select class='form-control' name='%s__gte' ><option value=''>------</option>""" % condition
    else:
        select_ele = """<select class='form-control' name='%s' ><option value=''>------</option>""" % condition


    # choices field
    if field_obj.choices:
        for choice_item in field_obj.choices:

            if str(choice_item[0]) == filter_conditions.get(condition):

                opt = '''<option value='%s' selected='selected' >%s</option>''' % (choice_item[0], choice_item[1])
            else:
                opt = '''<option value='%s' >%s</option>''' % (choice_item[0], choice_item[1])

            select_ele += opt

    if type(field_obj).__name__ == 'ForeignKey':
        for choice_item in field_obj.get_choices()[1:]:

            if str(choice_item[0]) == filter_conditions.get(condition):

                opt = '''<option value='%s' selected='selected' >%s</option>''' % (choice_item[0], choice_item[1])
            else:
                opt = '''<option value='%s' >%s</option>''' % (choice_item[0], choice_item[1])

            select_ele += opt
    #  时间
    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
        today = datetime.now().date()
        topt_list = [
            ['今天', today],
            ['过去1天', today - timedelta(days=1)],
            ['过去7天', today - timedelta(days=7)],
            ['这个月', today.replace(day=1)],
            ['过去30天', today - timedelta(days=30)],
            ['过去90天', today - timedelta(days=90)],
            ['过去180天', today - timedelta(days=180)],
            ['今年', today.replace(month=1, day=1)],
            ['过去一年', today.replace(year=today.year-1)],

        ]
        print('------------------------>', condition)
        for topt in topt_list:
            if str(topt[1]) == filter_conditions.get("%s__gte" % condition):

                opt = '''<option value='%s' selected='selected' >%s</option>''' % (topt[1], topt[0])
            else:
                opt = '''<option value='%s' >%s</option>''' % (topt[1], topt[0])

            select_ele += opt



    select_ele += "</select>"

    return mark_safe(select_ele)


@register.simple_tag
def create_get_url(filter_conditions):
    """
    拼接过滤条件url
    :param filter_conditions:
    :return:
    """
    url = ""
    for k, v in filter_conditions.items():
        url += "&%s=%s" % (k, v)
    # print("---------------->", url)
    return url


@register.simple_tag
def create_paginator_ele(query_sets, filter_url, oder_by_key):
    """
    拼接分页url
    :param query_sets:
    :param filter_url:
    :param oder_by_key:
    :return:
    """
    paginator_ele = ''
    add_dot_ele = False
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages-2 or \
                        abs(page_num - query_sets.number) <= 2:

            active_class = ''
            if page_num == query_sets.number:
                active_class = "active"
                add_dot_ele = False
            paginator_ele += '<li class="%s"><a href="?page=%s%s&o=%s">%s</a></li>' % (active_class, page_num, filter_url, oder_by_key, page_num)
        else:
            if not add_dot_ele:
                paginator_ele += '<li><span>...</span></li>'
                add_dot_ele = True
    return mark_safe(paginator_ele)
    # paginator_ele = ''
    # if query_sets.paginator.num_pages < 6:
    #     for i in range(query_sets.paginator.num_pages):
    #         if query_sets.number == i + 1:
    #             paginator_ele += '<li class="active"><a href="?page=%s%s">%s</a></li>' % (i + 1, filter_url, i + 1)
    #         else:
    #             paginator_ele += '<li><a href="?page=%s%s">%s</a></li>' % (i + 1, filter_url, i + 1)
    #     return mark_safe(paginator_ele)
    # paginator_head = ''
    # paginator_mid_head = ''
    # paginator_mid = ''
    # paginator_mid_foot = ''
    # paginator_foot = ""
    # for i in range(2):
    #     if query_sets.number == i + 1:
    #         paginator_head += '<li class="active"><a href="?page=%s%s">%s</a></li>' % (i+1, filter_url, i+1)
    #     else:
    #         paginator_head += '<li><a href="?page=%s%s">%s</a></li>' % (i + 1, filter_url, i + 1)
    #
    # for i in range(2):
    #     if query_sets.number == query_sets.paginator.num_pages - 1+i:
    #         paginator_foot += '<li class="active"><a href="?page=%s%s">%s</a></li>' % (query_sets.paginator.num_pages-1+i, filter_url, query_sets.paginator.num_pages-1+i)
    #     else:
    #         paginator_foot += '<li><a href="?page=%s%s">%s</a></li>' % (query_sets.paginator.num_pages - 1 + i, filter_url, query_sets.paginator.num_pages - 1 + i)
    #
    # for i in range(query_sets.number-2, query_sets.number+3):
    #     if 2 < i < query_sets.paginator.num_pages - 1:
    #
    #         if query_sets.number == i:
    #             paginator_mid += '<li class="active"><a href="?page=%s%s">%s</a></li>' % (i, filter_url, i)
    #         else:
    #             paginator_mid += '<li><a href="?page=%s%s">%s</a></li>' % (i, filter_url, i)



    # if query_sets.number > 5:
    #     paginator_mid_head = '<li><span>...</span></li>'
    #
    # if query_sets.number < query_sets.paginator.num_pages -4:
    #     paginator_mid_foot = '<li><span>...</span></li>'
    #
    # return mark_safe(paginator_head + paginator_mid_head + paginator_mid + paginator_mid_foot + paginator_foot)
@register.simple_tag
def get_field_tag(field):
    if field.field.required:
        label_str = field.label_tag(attrs={'class': 'col-sm-2 control-label'})
    else:
        label_str = field.label_tag(attrs={
            'class': 'col-sm-2 control-label',
            'style': "color:grey"
        })
    return label_str