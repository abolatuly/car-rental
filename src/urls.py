from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import pages.views
from src import settings

schema_view = get_schema_view(
   openapi.Info(
      title='Car Rental API',
      default_version='v1',
      contact=openapi.Contact(email='rentalcarkz@gmail.com'),
   ),
   public=True,
)

urlpatterns = [
    path('', pages.views.index, name='index'),
    path('about/', pages.views.about, name='about'),
    path('models/', pages.views.models, name='models'),
    path('reviews/', pages.views.reviews, name='reviews'),
    path('team/', pages.views.team, name='team'),
    path('contacts/', pages.views.contacts, name='contact'),
    path('account/', pages.views.account, name='account'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('src.api_urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
