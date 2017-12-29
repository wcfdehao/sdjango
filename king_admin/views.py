from django.shortcuts import render, redirect
from . import king_admin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from .function import table_filter, table_sort
from .forms import create_model_form
# Create your views here.


def index(request):
    # print(king_admin.king_admin_dict['crm']['customer'].model)
    return render(request, "king_admin/table_index.html", {'table_list': king_admin.king_admin_dict})


def display_table_objs(request, app_name, table_name):
    # print('----->', king_admin.king_admin_dict[app_name][table_name].model.objects.all())
    admin_class = king_admin.king_admin_dict[app_name][table_name]
    # object_list = admin_class.model.objects.all()
    object_list, filter_conditions = table_filter(request, admin_class, 'page', 'o')
    # 排序
    object_list, order_by_conditions = table_sort(request, admin_class, object_list)
    paginator = Paginator(object_list, admin_class.list_per_page)
    # print('---------------------')
    # print(paginator.page(1))
    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)
    # print('*****************')
    # print(query_sets)
    return render(request, 'king_admin/table_objs.html', {
        'admin_class': admin_class,
        'query_sets': query_sets,
        'filter_conditions': filter_conditions,
        'order_by_conditions': order_by_conditions,
        'app_name': app_name,
        'table_name': table_name,
    })


def table_obj_change(request, app_name, table_name, obj_id):
    admin_class = king_admin.king_admin_dict[app_name][table_name]
    model_form_class = create_model_form(request, admin_class)
    table_obj = admin_class.model.objects.get(id=obj_id)

    if request.method == 'POST':
        form_obj = model_form_class(request.POST, instance=table_obj)  # 更新
        # form_obj = model_form_class(request.POST) # 创建
        if form_obj.is_valid():
            form_obj.save()
            # redirect(reverse('king_admin:table_objs', args=(app_name, table_name)))

    else:
        form_obj = model_form_class(instance=table_obj)

    return render(request, 'king_admin/table_obj_change.html', {
        'table_obj': table_obj,
        'form_obj': form_obj,
        'admin_class': admin_class
    })

def table_obj_add(request, app_name, table_name):
    admin_class = king_admin.king_admin_dict[app_name][table_name]
    model_form_class = create_model_form(request, admin_class)

    if request.method == 'POST':
        form_obj = model_form_class(request.POST) # 创建
        if form_obj.is_valid():
            form_obj.save()
            # redirect(reverse('king_admin:table_objs', args=(app_name, table_name)))
            return redirect(reverse('king_admin:table_objs', args=(app_name, table_name)))

    else:
        form_obj = model_form_class()

    return render(request, 'king_admin/table_obj_add.html', {'form_obj': form_obj})

