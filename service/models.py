from django.db import models
from django.core import validators
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from collections import Counter
import numpy as np


'''
Class Customer

Properties:
    name
    sex
    age
    created_at

Methods:
    fetch_activity:
    fetch_monthly_activity:
'''
class Customer(models.Model):

    sex_choices = ((1,'男性'),(2,'女性'),)

    name = models.CharField('顧客名', max_length=100)
    sex  = models.IntegerField('性別', choices=sex_choices, default=1)
    age  = models.IntegerField('年齢',)
    created_at = models.DateField('登録日', auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def sex__str__(self):
        return dict(self.sex_choices)[self.sex]

    def fetch_monthly_activity(self, prev_month=0):
        today = date.today()
        first_day_of_month = today + relativedelta(months=prev_month) - timedelta(days=today.day-1)
        end_day_of_month   = today + relativedelta(months=prev_month+1) - timedelta(days=today.day)
        return self.fetch_activity(first_day_of_month, end_day_of_month)

    def fetch_activity(self, start_date, end_date):
        lessons = self.lessons.filter(date__gte=start_date, date__lte=end_date)
        lessons_count = len(lessons)
        total_charge = sum([l.charge for l in list(lessons)])
        lessons_counter = Counter([l.curriculum.name for l in list(lessons)])
        joint_genre = ""
        for k, v in lessons_counter.items():
            joint_genre = "%s%s(%s)/"%(joint_genre, k, v)

        if joint_genre.endswith('/'):
            joint_genre = joint_genre[:-1]

        return joint_genre, lessons_count, total_charge

'''
Class Curriculum

Properties:
    name

Methods:
    charge_calculator:
    programming_charge_calculator:
    english_charge_calculator:
    finance_charge_calculator:

'''

class Curriculum(models.Model):

    name = models.CharField('ジャンル', max_length=100)

    def __str__(self):
        return self.name

    def charge_calculator(self, total_hours, hours):
        if self.name == 'プログラミング':
            return self.programming_charge_calculator(total_hours+hours) - self.programming_charge_calculator(total_hours)
        elif self.name == '英語':
            return self.english_charge_calculator(total_hours+hours) - self.english_charge_calculator(total_hours)
        elif self.name == 'ファイナンス':
            return self.finance_charge_calculator(total_hours+hours) - self.finance_charge_calculator(total_hours)
        else:
            return 0

    def programming_charge_calculator(self, h):
        if h == 0:
            return 0
        elif h <= 5:
            return 20000
        elif h <= 20:
            return 20000 + (h - 5)*3500
        elif h <= 35:
            return 20000 + 15*3500 + (h-20)*3000
        elif h <= 50:
            return 20000 + 15*(3500+3000) + (h-35)*2800
        else:
            return 20000 + 15*(3500+3000+2800) + (h-50)*2500

    def english_charge_calculator(self, h):
        if h == 0:
            return 0
        else:
            return 5000 + 3500*h

    def finance_charge_calculator(self, h):
        if h <= 20:
            return 3300*h
        elif h <= 50:
            return 3300*20 + 2800*(h-20)
        else:
            return 3300*20 + 2800*30 + 2500*(h-50)


'''
Class Lesson

Properties:
    date
    hours
    charge

Methods:
    get_charge:
    check_update:
    report_calculator:

'''

class Lesson(models.Model):

    customer   = models.ForeignKey(Customer, verbose_name='顧客', related_name='lessons', on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, verbose_name='ジャンル', related_name='lessons', on_delete=models.CASCADE)

    date = models.DateField('日付')
    hours = models.IntegerField('時間', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(12)])
    charge = models.IntegerField('料金')

    def __str__(self):
        return self.customer.name

    def get_charge(self):
        the_day = self.date
        first_day_of_month = the_day + relativedelta(months=0) - timedelta(days=the_day.day-1)
        end_day_of_month   = the_day + relativedelta(months=1) - timedelta(days=the_day.day)

        lessons = Lesson.objects.filter(customer=self.customer, curriculum=self.curriculum, date__gte=first_day_of_month, date__lte=the_day)
        cumulated_hours = sum([i.hours for i in list(lessons) if not i == self]) # NOTE: 自分を除く. curriculum x dateのuidでunique validationとしてもよい？

        charge = self.curriculum.charge_calculator(cumulated_hours, self.hours)

        return charge

        """　もし受講時間を修正する場合、それよりも後に行った当月分の履修受講料を更新しなければならない　"""
    def check_update(self):
        the_day = self.date
        end_day_of_month   = the_day + relativedelta(months=1) - timedelta(days=the_day.day)

        lessons_to_update = Lesson.objects.filter(customer=self.customer, curriculum=self.curriculum, date__gt=the_day, date__lte=end_day_of_month)

        if lessons_to_update:
            for lesson_to_update in lessons_to_update:
                lesson_to_update.charge = lesson_to_update.get_charge()
                lesson_to_update.save()


def report_calculator(age_band_flg=False, prev_month=0):

    today = date.today()
    first_day_of_month = today + relativedelta(months=prev_month) - timedelta(days=today.day-1)
    end_day_of_month   = today + relativedelta(months=prev_month+1) - timedelta(days=today.day)

    lessons = Lesson.objects.filter(date__gte=first_day_of_month, date__lte=end_day_of_month).select_related()

    sex_choices = dict(((1,'男性'),(2,'女性'),))

    curriculums = Curriculum.objects.all()
    curriculum_choices = dict([(q.id, q.name) for q in curriculums ])

    data_array = []

    # 性別　x　ジャンル　レポート機能
    if age_band_flg:
        for s_k, s_v in sex_choices.items():
            for c_k, c_v in curriculum_choices.items():
                lesson_list = [l for l in list(lessons) if l.customer.sex == s_k and l.curriculum_id == c_k]
                age_list = [l.customer.age for l in lesson_list]
                bins = np.arange(10, 100, 10)
                age_bands = np.digitize(age_list, bins)

                for i in np.arange(1, 8):
                    lesson_at_age_band = []
                    for lesson, age_band in zip(lesson_list, age_bands):
                        if age_band == i:
                            lesson_at_age_band.append(lesson)

                    lesson_count = len(lesson_at_age_band)                                   # レッスン数
                    customer_count = len(set([l.customer for l in lesson_at_age_band ]))     # 受講者数
                    total_charge = sum([l.charge for l in lesson_at_age_band ])              # 売り上げ
                    data_array.append([s_v, c_v, bins[i-1], lesson_count, customer_count, total_charge])

    # 性別　x　ジャンル　レポート機能
    else:
        for s_k, s_v in sex_choices.items():
            for c_k, c_v in curriculum_choices.items():
                lesson_list = [l for l in list(lessons) if l.customer.sex == s_k and l.curriculum_id == c_k]
                lesson_count = len(lesson_list)                                   # レッスン数
                customer_count = len(set([l.customer for l in lesson_list ]))     # 受講者数
                total_charge = sum([l.charge for l in lesson_list ])              # 売り上げ
                data_array.append([s_v, c_v, lesson_count, customer_count, total_charge])

    return data_array
