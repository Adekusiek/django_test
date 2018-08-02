from django.urls import path
from . import views

app_name = 'service'
urlpatterns = [
    path('customer/', views.customer_list, name='customer_list'),
    path('customer/add', views.customer_edit, name='customer_add'),
    path('customer/mod/<int:customer_id>', views.customer_edit, name='customer_mod'),
    path('customer/del/<int:customer_id>', views.customer_del, name='customer_del'),

    path('lesson/', views.lesson_list, name='lesson_list'),
    path('lesson/add', views.lesson_edit, name='lesson_add'),
    path('lesson/mod/<int:lesson_id>', views.lesson_edit, name='lesson_mod'),
    path('lesson/del/<int:lesson_id>', views.lesson_del, name='lesson_del'),

    path('bill/', views.bill_list, name='bill_list'),
    path('report/', views.report_list, name='report_list'),

    path('', views.top, name='top'),


#     path('impression/<int:book_id>', views.ImpressionList.as_view(), name='impression_list'),
#     path('impression/add/<int:book_id>', views.impression_edit, name='impression_add'),
#     path('impression/mod/<int:book_id>/<int:impression_id>', views.impression_edit, name='impression_mod'),
#     path('impression/del/<int:book_id>/<int:impression_id>', views.impression_del, name='impression_del'),
]
