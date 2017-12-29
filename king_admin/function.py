# !usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'xinlan'
from django.db.models import Q


def table_filter(request, adimn_class, *args):
    """进行条件过滤，并返回过滤的数据"""
    filter_conditions = {}
    for k, v in request.GET.items():
        if v:
            filter_conditions[k] = v
    for reduce_arg in args:

        if reduce_arg in filter_conditions:
            del filter_conditions[reduce_arg]
    if 'q' in filter_conditions:
        find_args = filter_conditions['q']
        del filter_conditions['q']
        res = adimn_class.model.objects.filter(**filter_conditions)
        if find_args:
            q = Q()
            q.connector = 'OR'
            for field in adimn_class.search_fields:
                q.children.append(('%s__contains' % field, find_args))
            # print('------->',q)
            res = res.filter(q)
            filter_conditions['q'] = find_args
    else:
        res = adimn_class.model.objects.filter(**filter_conditions)

    res = res.order_by(adimn_class.ordering if adimn_class.ordering else "-id")

    # 搜索

    # value_columns = ''
    # for column in adimn_class.list_display:
    #     value_columns += column
    #     value_columns += ','

    # print('-------->','aaaaa')
    return res, filter_conditions


def table_sort(request, admin_class, objs):
    oderby_key = request.GET.get("o")
    if oderby_key:
        return objs.order_by(oderby_key), {'o': oderby_key}
    return objs, {'o': ''}
