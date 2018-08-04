from django.db import models
from django.core import validators
from collections import Counter


'''
Class Customer

Properties:
    name
    sex
    age
    created_at

Methods:
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

    def fetch_monthly_activity(self):
        lessons = self.lessons.all()
        lessons_count = len(lessons)
        total_charge = sum([l.charge for l in list(lessons)])
        lessons_counter = Counter([l.curriculum.name for l in list(lessons)])
        joint_genre = ""
        for k, v in lessons_counter.items():
            joint_genre = "%s%s(%s)/"%(joint_genre, k, v)

        if joint_genre.endswith('/'):
            joint_genre = joint_genre[:-1]

        return joint_genre, lessons_count, total_charge
