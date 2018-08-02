from django.db import models
from django.core import validators
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from collections import Counter

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

    # def fetch_monthly_activity(self, prev_month=3):
    #     today = date.today()
    #     first_day_of_month = today + relativedelta(months=1) - timedelta(days=today.day)

    def fetch_monthly_activity(self, start_date, end_date):
        lessons = self.lessons.filter(date__gte=start_date, date__lte=end_date)
        monthly_lessons_count = len(lessons)
        monthly_total_charge = sum([l.charge for l in list(lessons)])
        lessons_counter = Counter([l.curriculum.name for l in list(lessons)])
        monthly_genre = ""
        for k, v in lessons_counter.items():
            monthly_genre = "%s%s(%s)/"%(monthly_genre, k, v)

        return monthly_genre, monthly_lessons_count, monthly_total_charge

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

class Lesson(models.Model):

    customer   = models.ForeignKey(Customer, verbose_name='顧客', related_name='lessons', on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, verbose_name='ジャンル', related_name='lessons', on_delete=models.CASCADE)

    date = models.DateField('日付')
    hours = models.IntegerField('時間', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(12)])
    charge = models.IntegerField('料金')

    def __str__(self):
        return self.customer.name

    def get_charge(self):
        lessons = Lesson.objects.filter(customer=self.customer, curriculum=self.curriculum)
        cumulated_hours = sum([i.hours for i in list(lessons) if not i == self]) # 自分を除く

        # cumulated_hours = sum(list(customers.values_list('hours', flat=True)))
        charge = self.curriculum.charge_calculator(cumulated_hours, self.hours)

        return charge
