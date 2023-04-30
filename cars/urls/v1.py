from rest_framework.routers import DefaultRouter
from cars import views


router = DefaultRouter()
router.register(r'cars', views.CarViewSet)

urlpatterns = router.urls