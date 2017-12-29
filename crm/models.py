from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=32, blank=True, null=True)  # 32字节 blank限制django admin里可以为空
    qq = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=64, blank=True, null=True)

    source = models.ForeignKey("Source", verbose_name="流量渠道")
    referral_from = models.CharField(u"转介绍人qq", max_length=64, blank=True, null=True)

    course = models.ForeignKey("Course", verbose_name="咨询课程")
    customer_note = models.TextField(u'客户咨询详情', help_text=u'客户咨询的大概情况，和信息备注')

    tags = models.ManyToManyField("Tag", blank=True, null=True, verbose_name='意向标签')

    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    status_choice = (
        (0, '未报名'),
        (1, '已报名'),
    )
    status = models.SmallIntegerField(u'状态', choices=status_choice, default=0)
    date = models.DateTimeField(u'咨询日期', auto_now_add=True)

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name_plural = '客户表'


class Source(models.Model):
    """渠道表"""
    name = models.CharField(unique=True, max_length=32)


class Tag(models.Model):
    """意向标签"""
    name = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '标签'


class CustomerFollowUp(models.Model):
    """客户跟进表"""
    customer = models.ForeignKey("Customer")
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile")

    intention_choices = (
        (0, '2周内报名'),
        (1, '1个月内内报名'),
        (2, '近期无报名计划'),
        (3, '已在其他机构报名'),
        (4, '已报名'),
        (5, '已拉黑'),
    )
    intention = models.SmallIntegerField(choices=intention_choices)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s : %s>" % (self.customer, self.intention)

    class Meta:
        verbose_name_plural = '客户跟进'


class Course(models.Model):
    """课程信息"""
    name = models.CharField(u'课程名称', max_length=64, unique=True)
    price = models.PositiveSmallIntegerField(u"学费")
    period = models.PositiveSmallIntegerField(u"学时")
    outline = models.TextField(u'课程大纲', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '课程信息'


class Branch(models.Model):
    """校区"""
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '校区'


class ClassList(models.Model):
    """班级"""
    branch = models.ForeignKey("Branch", verbose_name="分校")
    course = models.ForeignKey("Course")
    class_type_choice = (
        (0, '面授(脱产)'),
        (1, '面授(周末)'),
        (2, '网络班'),
    )
    class_type = models.SmallIntegerField(choices=class_type_choice, verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="结业日期", blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)

    class Meta:
        unique_together = ('branch', 'course', 'semester')  # 联合唯一
        verbose_name_plural = '班级'


class CourseRecord(models.Model):
    """上课记录"""
    from_class = models.ForeignKey('ClassList', verbose_name='班级')
    day_num = models.PositiveSmallIntegerField(verbose_name='第几节(天)')
    teacher = models.ForeignKey("UserProfile")
    outline = models.TextField(verbose_name="本节课题")
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)

    max_num = models.PositiveSmallIntegerField(verbose_name='最高人数')
    before_ad_num = models.PositiveSmallIntegerField(verbose_name='广告前人数')

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.from_class, self.day_num)

    class Meta:
        unique_together = ('from_class', 'day_num')
        verbose_name_plural = '上课记录'


class StudyRecord(models.Model):
    """学习记录"""
    student = models.ForeignKey("Enrollment")
    course_record = models.ForeignKey("CourseRecord")
    attendance_choice = (
        (0, '已签到'),
        (1, '迟到'),
        (2, '缺勤'),
        (3, '早退'),

    )
    attendance = models.SmallIntegerField(choices=attendance_choice, default=0)
    score_choice = (
        (100, "A+"),
        (90, "A"),
        (85, "B+"),
        (80, "B"),
        (75, "B-"),
        (70, "C+"),
        (60, "C"),
        (40, "C-"),
        (-50, "D"),
        (-100, "COPY"),
        (0, "N/A"),
    )
    score = models.SmallIntegerField(choices=score_choice, default=0)
    memo = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.student, self.course_record, self.score)

    class Meta:
        unique_together = ('student', 'course_record')
        verbose_name_plural = '学习记录'


class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey("Customer")
    enrolled_class = models.ForeignKey("ClassList", verbose_name="所报班级")

    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    contract_agreed = models.BooleanField(default=False, verbose_name="学员已同意合同条款")
    contract_approved = models.BooleanField(default=False, verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.enrolled_class)

    class Meta:
        unique_together = ('customer', 'enrolled_class')
        verbose_name_plural = "报名表"


class Payment(models.Model):
    """缴费记录"""
    customer = models.ForeignKey("Customer")
    course = models.ForeignKey("Course")
    amount = models.PositiveIntegerField(verbose_name="数额", default=500)
    consultant = models.ForeignKey("UserProfile")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.amount)

    class Meta:
        verbose_name_plural = "报名表"


class UserProfile(models.Model):
    """用户信息表"""
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role', blank=True, null=True)
    qq = models.CharField(max_length=32,  blank=True, null=True)
    phone = models.CharField(max_length=32,  blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "用户信息"


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField("Menu", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色表"


class Menu(models.Model):
    """菜单表"""
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "菜单"
