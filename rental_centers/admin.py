from django.contrib import admin
from .models import RentalCenter


class RentalCenterAdmin(admin.ModelAdmin):
    list_display = ('location', 'is_active')
    list_editable = ('is_active', )
    search_fields = ('location',)


admin.site.register(RentalCenter, RentalCenterAdmin)
