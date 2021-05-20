from django.contrib import admin

# Register your models here.
from admin_profile.models import Error


@admin.register(Error)
class ErrorMessage(admin.ModelAdmin):
    list_display = ('date', 'message',)