from django.db import models
from django.core import validators
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from .customer import Customer
from .curriculum import Curriculum


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

    """　
        もし受講時間を修正する場合、それよりも後に行った当月分の履修受講料を更新しなければならない
        レッスンの更新がかかった時呼び出される
    """

    def check_update(self):
        the_day = self.date
        end_day_of_month   = the_day + relativedelta(months=1) - timedelta(days=the_day.day)

        lessons_to_update = Lesson.objects.filter(customer=self.customer, curriculum=self.curriculum, date__gt=the_day, date__lte=end_day_of_month)

        if lessons_to_update:
            for lesson_to_update in lessons_to_update:
                lesson_to_update.charge = lesson_to_update.get_charge()
                lesson_to_update.save()
