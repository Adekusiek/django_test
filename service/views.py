from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Customer, Lesson
from .models import report_calculator
from .forms import CustomerForm, LessonForm

def top(request):
    return render(request, 'service/top/top.html', {})

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



def lesson_index(request):
    lessons = Lesson.objects.all().order_by('id')
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

def bill_index(request):
    customers = Customer.objects.all().select_related().order_by('id')
    customer_activities = []
    for customer in customers:
        customer_activities.append(customer.fetch_monthly_activity())

    customer_infos = zip(customers, customer_activities)
    return render(request, 'service/bill/index.html', {'customer_infos': customer_infos})

def report_index(request):

    sex_genre_array = report_calculator()
    sex_genre_ageband_array = report_calculator(age_band_flg=True)

    return render(request, 'service/report/index.html', {'sex_genre_array': sex_genre_array, 'sex_genre_ageband_array': sex_genre_ageband_array})
