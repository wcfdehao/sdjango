# !usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'xinlan'
from django.utils.timezone import timedelta, datetime
from .models import Word, Record
import requests

config = {
        0: timedelta(days=1),
        1: timedelta(days=3),
        2: timedelta(days=7),
        3: timedelta(days=15),
        4: timedelta(days=30),
        5: timedelta(days=90),
        6: timedelta(days=180)
    }

def spider_word_by_name(name):
    if name.isalpha():
        url = 'http://fanyi.baidu.com/v2transapi'
        data = {
            'from':'en',
            'to': 'zh',
            'query': name,
            'transtype': 'realtime',
            'simple_means_flag': 3
        }
        response = requests.post(url, data=data)
        data = response.json()
        # print(data['dict_result']['simple_means']['is_CRI'])

        try:
            means = ''
            for item in data['dict_result']['simple_means']['symbols'][0]['parts']:

                means += item['part']+' '+str(item['means'])+' '
            try:
                word = Word(
                    word=name,
                    means=means
                )
                word.save()
                return {'id': word.id, 'means': means}
            except Exception as e:
                print(e)
                return {'id': '', 'means': '未知错误请重试'}
        except Exception as e:
            print(e)
            return {'id': '', 'means': '没有这个单词！'}
    return {'id': '', 'means': '没有这个单词！'}


def update_record_status(request):

    records = Record.objects.filter(user=request.user, type__range=(0, 7))
    today = datetime.now().date()
    for record in records:

        if today - config[record.type] == record.c_time.date():
            record.status = 1
        elif today - config[record.type] > record.c_time.date():
            record.status = 2
        else:
            record.status = 0
        record.save()


def record_is_need_review(record, **kwargs):

    if datetime.now().date() - config[record.type] >= record.c_time.date():
        return record

if __name__ == '__main__':
    spider_word_by_name('word')
