from django.urls import path, include

urlpatterns = [
    path('', include('users.urls.v1')),
    path('', include('cars.urls.v1')),
    path('', include('rental_centers.urls.v1')),
    path('', include('orders.urls.v1')),
    path('', include('payments.urls.v1')),
    path('', include('damage_detection.urls.v1')),
]