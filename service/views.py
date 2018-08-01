from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Customer, Lesson
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
