from django.urls import path
from . import views

app_name = 'service'
urlpatterns = [
    path('customers/', views.customer_index, name='customer_index'),
    path('customer/add', views.customer_edit, name='customer_add'),
    path('customer/mod/<int:customer_id>', views.customer_edit, name='customer_mod'),
    path('customer/del/<int:customer_id>', views.customer_del, name='customer_del'),

    path('lessons/', views.lesson_index, name='lesson_index'),
    path('lesson/add', views.lesson_edit, name='lesson_add'),
    path('lesson/mod/<int:lesson_id>', views.lesson_edit, name='lesson_mod'),
    path('lesson/del/<int:lesson_id>', views.lesson_del, name='lesson_del'),

    path('bills/', views.bill_index, name='bill_index'),
    path('reports/', views.report_index, name='report_index'),

    path('', views.top, name='top'),

]
