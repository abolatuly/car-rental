from rest_framework.routers import DefaultRouter
from rental_centers import views


router = DefaultRouter()
router.register(r'rental-centers', views.RentalCenterViewSet)

urlpatterns = router.urls