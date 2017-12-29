from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=32, blank=True, null=True)  # 32字节 blank限制django admin里可以为空
    qq = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    sexy_type = (('male', u'男性'), ('female', u'女性'))
    sexy = models.CharField(u'性别', choices=sexy_type, default='male', max_length=32)
    birthday = models.DateField(u'生日', blank=True, null=True, help_text='格式yyyy-mm-dd')
    email = models.CharField(u'常用邮箱', blank=True, null=True)
    card_num = models.CharField(u'身份证号码', blank=True, null=True, max_length=64)
    work_status_choices = (('employed', '在职'), ('unemployed', '无业'), ('student', '学生'), ('interest', '兴趣'), ('unknown', '未知'))
    work_status = models.CharField(u"职业状态", choices=work_status_choices, max_length=32, default='unknown')

    source = models.ForeignKey("Source", verbose_name="流量渠道")
    referral = models.ForeignKey('self', verbose_name="转介绍学员", help_text=u"若此客户是转介绍自内部学员,请在此处选择内部＼学员姓名", blank=True, null=True, related_name="internal_referral")

    course = models.ForeignKey("Course", verbose_name=u"咨询课程")
    cousult_content = models.TextField(u"咨询详情", help_text=u"客户咨询的大概情况,客户个人信息备注等...")
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="意向等级")

    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")

    status_choice = (
        (0, '未报名'),
        (1, '已报名'),
    )
    status = models.SmallIntegerField(u'状态', choices=status_choice, default=0)
    date = models.DateTimeField(u"录入日期", auto_now_add=True)

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name_plural = '客户表'


class Source(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '流量渠道'


class Tag(models.Model):
    """意向等级"""
    name = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '意向等级'


class CustomerFollowUp(models.Model):
    """客户跟进表"""
    customer = models.ForeignKey("Customer")
    content = models.TextField(u"跟进内容")
    consultant = models.ForeignKey("UserProfile", verbose_name="跟进人")

    status_choices = (
        (0, '2周内报名'),
        (1, '1个月内内报名'),
        (2, '近期无报名计划'),
        (3, '已在其他机构报名'),
        (4, '已报名'),
        (5, '已拉黑'),
    )
    status = models.SmallIntegerField(u'状态', choices=status_choices, help_text=u'选择客户此时的状态')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s : %s>" % (self.customer, self.status)

    class Meta:
        verbose_name_plural = '客户跟进'


class Course(models.Model):
    """课程信息"""
    name = models.CharField(max_length=64, unique=True)
    period = models.PositiveSmallIntegerField(verbose_name="周期")
    outline = models.TextField()
    college = models.ForeignKey('College')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '课程信息'


class College(models.Model):
    """学院"""
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '学院'


class ClassList(models.Model):
    """班级"""
    college = models.ForeignKey("College", verbose_name=u"学院")
    course = models.ForeignKey(u'课程', "Course")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    price = models.PositiveSmallIntegerField(u'价格')
    teachers = models.ManyToManyField("UserProfile", blank=True, null=True)
    start_date = models.DateField("开班日期")
    end_date = models.DateField(verbose_name="结业日期", blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)

    class Meta:
        unique_together = ('college', 'course', 'semester')  # 联合唯一
        verbose_name_plural = '班级'


class PayType(models.Model):
    """支付方式"""
    name = models.CharField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'支付方式'


class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey("Customer")
    enrolled_class = models.ForeignKey("ClassList", verbose_name=u"所报班级")

    consultant = models.ForeignKey("UserProfile", verbose_name=u"签单客服")
    teacher = models.ForeignKey("UserProfile", verbose_name=u"公开课讲师")
    flow_consultant = models.ForeignKey("UserProfile", verbose_name=u'助教')

    is_in_class = models.BooleanField(u'课堂报名', default=False)
    # contract_agreed = models.BooleanField(default=False, verbose_name="学员已同意合同条款")
    # contract_approved = models.BooleanField(default=False, verbose_name="合同已审核")

    pay_type = models.ForeignKey("PayType", verbose_name=u"支付方式")
    status_choices = (
        (0, u'预订'),
        (1, u'欠款'),
        (2, u'退学'),
        (3, u'完成')
    )
    status = models.SmallIntegerField(u"状态", choices=status_choices, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.enrolled_class)

    class Meta:
        unique_together = ('customer', 'enrolled_class')
        verbose_name_plural = "报名表"


class PaymentRecord(models.Model):
    """缴费记录"""
    enrollment = models.ForeignKey("Enrollment")
    pay_type_choices = ((0, u"订金/报名费"),
                        (1, u"补学费"),
                        (2, u"退款"),
                        )
    pay_type = models.CharField("费用类型", choices=pay_type_choices, max_length=64, default=0)

    amount = models.PositiveIntegerField(u"数额", default=500)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.enrollment, self.pay_type, self.amount)

    class Meta:
        verbose_name_plural = "缴费记录"


class UserProfile(models.Model):
    """用户信息表"""
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role', blank=True, null=True)

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
    order = models.SmallIntegerField(u'排序', default=999)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "菜单"


#
#
# class CourseRecord(models.Model):
#     """上课记录"""
#     from_class = models.ForeignKey('ClassList', verbose_name='班级')
#     day_num = models.PositiveSmallIntegerField(verbose_name='第几节(天)')
#     teacher = models.ForeignKey("UserProfile")
#     outline = models.TextField(verbose_name="本节课题")
#     has_homework = models.BooleanField(default=True)
#     homework_title = models.CharField(max_length=128, blank=True, null=True)
#     homework_content = models.TextField(blank=True, null=True)
#
#     max_num = models.PositiveSmallIntegerField(verbose_name='最高人数')
#     before_ad_num = models.PositiveSmallIntegerField(verbose_name='广告前人数')
#
#     date = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return "%s %s" % (self.from_class, self.day_num)
#
#     class Meta:
#         unique_together = ('from_class', 'day_num')
#         verbose_name_plural = '上课记录'
#
#
# class StudyRecord(models.Model):
#     """学习记录"""
#     student = models.ForeignKey("Enrollment")
#     course_record = models.ForeignKey("CourseRecord")
#     attendance_choice = (
#         (0, '已签到'),
#         (1, '迟到'),
#         (2, '缺勤'),
#         (3, '早退'),
#
#     )
#     attendance = models.SmallIntegerField(choices=attendance_choice, default=0)
#     score_choice = (
#         (100, "A+"),
#         (90, "A"),
#         (85, "B+"),
#         (80, "B"),
#         (75, "B-"),
#         (70, "C+"),
#         (60, "C"),
#         (40, "C-"),
#         (-50, "D"),
#         (-100, "COPY"),
#         (0, "N/A"),
#     )
#     score = models.SmallIntegerField(choices=score_choice, default=0)
#     memo = models.TextField(blank=True, null=True)
#     date = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return "%s %s %s" % (self.student, self.course_record, self.score)
#
#     class Meta:
#         unique_together = ('student', 'course_record')
#         verbose_name_plural = '学习记录'
