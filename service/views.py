from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Customer, Lesson
from .models import sex_genre_calculator
from .forms import CustomerForm, LessonForm

def top(request):
    return render(request, 'service/top/top.html', {})

def customer_list(request):
    customers = Customer.objects.all().order_by('id')
    return render(request, 'service/customer/list.html', {'customers': customers})

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
            return redirect('service:customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'service/customer/edit.html', dict(form=form, customer_id=customer_id))

def customer_del(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return redirect('service:customer_list')



def lesson_list(request):
    lessons = Lesson.objects.all().order_by('id')
    return render(request, 'service/lesson/list.html', {'lessons': lessons})

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

            return redirect('service:lesson_list')
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'service/lesson/edit.html', dict(form=form, lesson_id=lesson_id))

def lesson_del(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lesson.delete()
    return redirect('service:lesson_list')

def bill_list(request):
    customers = Customer.objects.all().select_related().order_by('id')
    customer_activities = []
    for customer in customers:
        customer_activities.append(customer.fetch_monthly_activity())

    customer_infos = zip(customers, customer_activities)
    return render(request, 'service/bill/list.html', {'customer_infos': customer_infos})

def report_list(request):

    sex_genre_array = sex_genre_calculator()

    return render(request, 'service/report/list.html', {'sex_genre_array': sex_genre_array})
