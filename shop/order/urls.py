from django.urls import path

from order.views import order_create

from . import views

app_name = 'order'
urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('history/', views.OrderList.as_view(), name='order_history')
]
