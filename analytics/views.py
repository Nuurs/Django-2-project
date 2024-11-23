from django.shortcuts import render
from .models import ApiRequest
from django.db.models import Count

def analytics_dashboard(request):
    # Get active users
    active_users = ApiRequest.objects.values('user').annotate(request_count=Count('id')).order_by('-request_count')
    
    # Optionally, add other analytics data here

    return render(request, 'analytics/dashboard.html', {'active_users': active_users})
