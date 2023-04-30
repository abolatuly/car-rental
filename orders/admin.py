from django.contrib import admin
from . import models


class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'status')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('user', 'number')
    ordering = ('status',)


class CustomOrderItemAdmin(admin.ModelAdmin):
    list_display = ('car', 'pick_up_location', 'drop_off_location', 'pick_up_date', 'drop_off_date', 'amount')
    list_filter = ('pick_up_location', 'drop_off_location')
    ordering = ('pick_up_date',)


admin.site.register(models.Order, CustomOrderAdmin)
admin.site.register(models.OrderItem, CustomOrderItemAdmin)
