from django.contrib import admin

# Register your models here.
from admission.models import Grade, Profile, File, Participant, FirstTourDates, Group, Olympiad


@admin.register(Grade)
class AdminGrade(admin.ModelAdmin):
    list_display = ('number', 'profile_id')
    sortable_by = ('number', 'profile_id')


admin.site.register(File)
admin.site.register(Participant)
admin.site.register(FirstTourDates)
admin.site.register(Group)
admin.site.register(Profile)
admin.site.register(Olympiad)
