from django.contrib import admin

from first_tour.models import Tour


class TourOrderAdminFilter(admin.FieldListFilter):
    title = 'Tours'
    parameter_name = 'tour_order_admin_filter'

    def lookups(self, request, model_admin):
        return [tour.tour_order for tour in Tour.objects.all().distinct('tour_order')]

    def queryset(self, request, queryset):
        return queryset.filter(tour__tour_order=self.value())
