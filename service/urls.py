from django.urls import path
from . import views

app_name = 'service'
urlpatterns = [
    path('customer/', views.customer_list, name='customer_list'),
    path('customer/add', views.customer_edit, name='customer_add'),
    path('customer/mod/<int:customer_id>', views.customer_edit, name='customer_mod'),
    path('customer/del/<int:customer_id>', views.customer_del, name='customer_del'),
    path('', views.top, name='top'),


#     path('impression/<int:book_id>', views.ImpressionList.as_view(), name='impression_list'),
#     path('impression/add/<int:book_id>', views.impression_edit, name='impression_add'),
#     path('impression/mod/<int:book_id>/<int:impression_id>', views.impression_edit, name='impression_mod'),
#     path('impression/del/<int:book_id>/<int:impression_id>', views.impression_del, name='impression_del'),
]
