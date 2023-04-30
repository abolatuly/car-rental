from django.contrib import admin
from payments import models


class CustomBillAdmin(admin.ModelAdmin):
    list_display = ('order', 'number', 'total', 'status')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('number',)
    ordering = ('status',)


admin.site.register(models.Bill, CustomBillAdmin)
