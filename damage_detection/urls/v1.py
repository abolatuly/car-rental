from django.urls import path
from rest_framework.routers import DefaultRouter
from damage_detection import views


router = DefaultRouter()
router.register(r'damage-detection', views.DamageDetectionViewSet)

urlpatterns = [
    path('damage-detection/<order_id>/', views.DamageDetectionViewSet.as_view({'get': 'retrieve'}))
] + router.urls
