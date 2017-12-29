# !usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'xinlan'
from django.forms import forms, ModelForm

from crm import models

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


def create_model_form(request, admin_class):
    """
    动态的生成form
    :param request:
    :param admin_class:
    :return:
    """
    class Meta:
        model = admin_class.model
        fields = "__all__"

    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'

        return ModelForm.__new__(cls)
            # field.field.widget.attrs['class'] = 'form-control'
    _model_form_class = type("MyModelForm", (ModelForm,), {"Meta": Meta, '__new__': __new__})
    # setattr(_model_form_class, 'Meta', Meta)
    # n.field.widget.attrs['class']='aaaa'
    # n.label_tag(attrs={'class': 'ccc'})

    return _model_form_class
