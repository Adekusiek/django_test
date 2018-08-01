from django.forms import ModelForm
from .models import Customer, Lesson


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = ('name', 'sex', 'age',)

class LessonForm(ModelForm):

    class Meta:
        model = Lesson
        fields = ('customer', 'curriculum', 'hours', 'date', )
