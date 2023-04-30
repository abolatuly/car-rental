from django.contrib import admin
from . import models


class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('name', 'data')


admin.site.register(models.Car, CarAdmin)