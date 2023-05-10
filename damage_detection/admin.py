from django.contrib import admin
from . import models


class CustomDamageDetectionAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'data')
    fieldsets = [
        (None, {'fields': ['order', 'status', 'data', 'front_image', 'left_image', 'right_image', 'back_image']}),
    ]
    list_filter = ('status',)
    search_fields = ('order',)
    ordering = ('-created_at',)


admin.site.register(models.DamageDetection, CustomDamageDetectionAdmin)
