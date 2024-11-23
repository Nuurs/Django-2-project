from django.contrib import admin
from .models import ApiRequest
from django.db.models import Count

class ApiRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_count')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Add the request count annotation
        queryset = queryset.values('user').annotate(request_count=Count('id')).order_by('-request_count')
        return queryset

admin.site.register(ApiRequest, ApiRequestAdmin)
