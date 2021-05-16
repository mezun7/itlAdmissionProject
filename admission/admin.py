from django.contrib import admin

# Register your models here.
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline

from admission.actions import export_as_xls, export_as_xls_full_participant_data
from admission.models import Profile, File, Participant, FirstTourDates, Group, Olympiad, Moderator, \
    ModeratorMessage, ParticipantRegistrator


class FileAdmin(TabularInline):
    model = Participant.portfolio.through

#
# @admin.register(Grade)
# class AdminGrade(admin.ModelAdmin):
#     list_display = ('number', 'profile_id')
#     sortable_by = ('number', 'profile_id')


@admin.register(Participant)
class AdminParticipant(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_name', 'first_name', 'fathers_name', 'grade',
                    'profile', 'first_tour_register_date', 'get_email', 'reg_status',
                    'is_dublicate', 'first_tour_come_date', "extra_score")
    sortable_by = ('grade', 'last_name', 'first_name',)
    list_filter = ('grade', 'profile', 'first_tour_register_date', 'out_of_competition', 'reg_status', 'privilege_status')
    search_fields = ['user__username','first_name', 'last_name']
    exclude = ['portfolio']
    inlines = [
        FileAdmin,
    ]
    actions = [export_as_xls, export_as_xls_full_participant_data]

    def get_email(self, participant):
         return str(participant.user.email)

    get_email.short_description = 'email'
    get_email.admin_order_field = 'book__author'


@admin.register(ModeratorMessage)
class AdminModeratorMessage(admin.ModelAdmin):
    list_display = ('sent_at', 'moderator', 'participant', 'verdict')


@admin.register(Moderator)
class AdminModerator(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(File)
admin.site.register(FirstTourDates)
admin.site.register(Group)
admin.site.register(Profile)
admin.site.register(Olympiad)
admin.site.register(ParticipantRegistrator)