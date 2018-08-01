from django.db import models
from django.core import validators

class Customer(models.Model):

    sex_choices = ((1,'男性'),(2,'女性'),)

    name = models.CharField('顧客名', max_length=100)
    sex  = models.IntegerField('性別', choices=sex_choices, default=1)
    age  = models.IntegerField('年齢',)
    created_at = models.DateField('登録日', auto_now_add=True)

    def __str__(self):
        return self.name

    def sex__str__(self):
        return dict(self.sex_choices)[self.sex]

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


class Curriculum(models.Model):

    name = models.CharField('ジャンル', max_length=100)

    def __str__(self):
        return self.name

class Lesson(models.Model):

    customer   = models.ForeignKey(Customer, verbose_name='顧客', related_name='lessons', on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, verbose_name='ジャンル', related_name='lessons', on_delete=models.CASCADE)

    date = models.DateField('日付')
    hours = models.IntegerField('時間', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(12)])
    charge = models.IntegerField('料金')

    def __str__(self):
        return self.customer.name
