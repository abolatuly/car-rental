from django.urls import path
from rest_framework.routers import DefaultRouter
from orders import views


router = DefaultRouter()
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('orders/<order_id>/complete/', views.OrderViewSet.as_view({'post': 'complete_order'})),
    path('orders/<order_id>/cancel/', views.OrderViewSet.as_view({'post': 'cancel_order'})),
] + router.urls
