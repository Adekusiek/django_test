from django.db import models
from django.core import validators

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
