# !usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'xinlan'
from crm.models import Customer, UserProfile


king_admin_dict = {}  # {'appname': {'table_name': admin_class}}

class BaseAdmin:
    list_display = []
    list_filter = []
    list_per_page = 10
    search_fields = []
    filter_horizontal = []
    ordering = None

    def __init__(self, model):
        self.model = model
        self.opts = model._meta



class CustomerAdmin(BaseAdmin):
    list_display = ('id', 'qq', 'source', 'consultant', 'content', 'status', 'date')
    list_filter = ('source', 'consultant', 'date')
    search_fields = ('name', 'qq', 'consultant__name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status', )
    list_per_page = 5
    # ordering = "-id"


class UserProfileAdmin(BaseAdmin):
    list_display = ('user', 'name')


def register(models_class, admin_class=None):
    global king_admin_dict
    appname = models_class._meta.app_label
    if appname not in king_admin_dict:
        king_admin_dict[appname] = {}

    king_admin_dict[appname][models_class._meta.model_name] = admin_class(models_class)


register(Customer, CustomerAdmin)
register(UserProfile, UserProfileAdmin)