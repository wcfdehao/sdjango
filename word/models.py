from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Word(models.Model):
    """单词表"""
    word = models.CharField(max_length=32, unique=True)
    means = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)


class Record(models.Model):
    """背诵记录表"""
    user = models.ForeignKey(User)
    num = models.SmallIntegerField(verbose_name="个数")
    type_choices = (
        (0, '首次'),
        (1, '1天'),
        (2, '3天'),
        (3, '7天'),
        (4, '15天'),
        (5, '1月'),
        (6, '3月'),
        (7, '半年'),

    )
    type = models.SmallIntegerField(choices=type_choices, default=0, verbose_name="类型")
    status_choices = (
        (0, '正常'),
        (1, '复习'),
        (2, '未及时'),
    )
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="状态")  # 0是正常状态, 1表示需要复习,2表示没有及时复习
    test_times = models.IntegerField(default=0, verbose_name="次数")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="时间")


class RecordDetail(models.Model):
    """背诵记录详细表"""
    record = models.ForeignKey("Record")
    word = models.ForeignKey("Word")