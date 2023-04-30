from rest_framework.routers import DefaultRouter
from orders import views


router = DefaultRouter()
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'order', views.OrderViewSet)

urlpatterns = router.urls
