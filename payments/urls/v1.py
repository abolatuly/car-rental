from django.urls import path
from payments import views


urlpatterns = [
    path('bills/<order_id>/', views.BillViewSet.as_view({'get': 'get_bill'})),
    path('bills/<order_id>/pay/', views.BillViewSet.as_view({'post': 'pay_bill'})),
]