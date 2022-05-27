from django.contrib import admin
from .models import LiterGradeTutor


# @admin.register(LiterGradeRegistrar)
class LiterGradeRegistrarAdmin(admin.ModelAdmin):
    list_display = ('litergrade', 'participantregistrator')


admin.site.register(LiterGradeTutor, LiterGradeRegistrarAdmin)


