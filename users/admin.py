from django.contrib import admin
from . import models


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'date_of_birth')
    fieldsets = [
        (None, {'fields': ['email', 'first_name', 'last_name', 'phone_number', 'date_of_birth']}),
    ]
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(models.CustomUser, CustomUserAdmin)
