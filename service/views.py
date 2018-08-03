from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from .models import Customer, Lesson
from .forms import CustomerForm, LessonForm
from .utils import get_month_array, get_start_end_month, report_calculator


def top(request):
    return render(request, 'service/top/top.html')

''' customer view '''

def customer_index(request):
    customers = Customer.objects.all().order_by('id')
    return render(request, 'service/customer/index.html', {'customers': customers})

def customer_edit(request, customer_id=None):
    if customer_id:
        customer = get_object_or_404(Customer, pk=customer_id)
    else:
        customer = Customer()

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('service:customer_index')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'service/customer/edit.html', dict(form=form, customer_id=customer_id))

def customer_del(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return redirect('service:customer_index')

''' lesson view '''

def lesson_index(request):
    lessons = Lesson.objects.all().order_by('id').select_related()
    return render(request, 'service/lesson/index.html', {'lessons': lessons})

def lesson_edit(request, lesson_id=None):
    if lesson_id:
        lesson = get_object_or_404(Lesson, pk=lesson_id)
    else:
        lesson = Lesson()

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.charge = lesson.get_charge()
            lesson.save()
            if lesson_id:
                lesson.check_update()

            return redirect('service:lesson_index')
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'service/lesson/edit.html', dict(form=form, lesson_id=lesson_id))

def lesson_del(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lesson.delete()
    return redirect('service:lesson_index')


''' bill view '''

def bill_index(request):

    # prepare an array to show year-month choice
    month_infos = get_month_array()

    prev_month = 0
    if request.GET.get('prev_month'):
        prev_month = int(request.GET.get('prev_month'))

    start_date, end_date = get_start_end_month(prev_month)

    customers = Customer.objects.prefetch_related(Prefetch("lessons", queryset=Lesson.objects.filter(date__gte=start_date, date__lte=end_date).select_related('curriculum'))).order_by('id')

    customer_activities = []
    for customer in customers:
        customer_activities.append(customer.fetch_monthly_activity())

    customer_infos = zip(customers, customer_activities)

    return render(request, 'service/bill/index.html', {'customer_infos': customer_infos, 'month_infos': month_infos})



''' report view '''

def report_index(request):

    month_infos = get_month_array()
    prev_month = 0
    if request.GET.get('prev_month'):
        prev_month = int(request.GET.get('prev_month'))

    sex_genre_array = report_calculator(prev_month=prev_month)
    sex_genre_ageband_array = report_calculator(age_band_flg=True, prev_month=prev_month)

    return render(request, 'service/report/index.html', {'sex_genre_array': sex_genre_array, 'sex_genre_ageband_array': sex_genre_ageband_array, 'month_infos': month_infos})
