from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Word, Record, RecordDetail
from .functions import spider_word_by_name, update_record_status
from .functions import record_is_need_review
from django.core.urlresolvers import reverse
from django.utils.timezone import datetime
# Create your views here.


def index(request):

    return render(request, "word/index.html")


def create_record(request):
    """
    创建单词背诵记录
    :param request:
    :return:
    """

    if request.method == 'GET':

        return render(request, "word/create_record.html")

    if request.method == 'POST':
        if Record.objects.last().c_time.date() != datetime.now().date():

            ids = request.POST.getlist('ids[]')
            ids = set(ids)  # 去重
            record = Record.objects.create(
                user=request.user,
                num=len(ids),
                type=0,
            )
            try:
                for word_id in ids:

                    record_detail = RecordDetail.objects.create(

                        record=record,
                        word=Word.objects.get(pk=word_id)
                    )
                    record_detail.save()
                    info = {'status': True, 'info': '创建成功！', 'url': reverse('word:record_list')}
            except Exception as e:

                info = {'status': False, 'info': '创建失败，请重新尝试！'}
        else:
            info = {'status': False, 'info': '每天只能创建一个背诵记录'}
        return JsonResponse(info)


def get_word_by_name(request):
    """通过单词名称获取单词信息"""
    if request.method == 'POST':
        name = request.POST['name']
        name = name.lower()
        try:
            word = Word.objects.get(word=name)
            info = {'id': word.id, 'means': word.means}
        except Word.DoesNotExist as e:
            info = spider_word_by_name(name)
        return JsonResponse(info)


def record_list(request):
    """背诵列表"""
    update_record_status(request)
    records = Record.objects.filter(user=request.user, type__range=(0, 7), status__in=[1, 2]).order_by('-c_time')
    type_choies = Record.type_choices
    status_choies = Record.status_choices
    return render(request, 'word/record_list.html', {
        'records': records,
        'type_choies': type_choies,
        'status_choies': status_choies,
    })


def record_detail(request, record_id):
    """背诵列表详情"""
    record = Record.objects.get(pk=record_id)
    record_details = record.recorddetail_set.all()
    return render(request, 'word/record_detail.html', {
        'record_details': record_details,
        'record': record
    })


def review(request, record_id):
    record = Record.objects.get(pk=record_id)
    if record_is_need_review(record):
        if record.type < Record.type_choices[-1][0]:
            record.type += 1

        record.status = 0
        record.save()
    else:
        print('---------------------->')

    return redirect(reverse('word:record_list'))

