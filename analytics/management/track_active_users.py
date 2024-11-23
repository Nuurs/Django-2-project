from django.core.management.base import BaseCommand
from analytics.models import ApiRequest
from django.db.models import Count

class Command(BaseCommand):
    help = 'Tracks active users based on API request count'

    def handle(self, *args, **kwargs):
        active_users = ApiRequest.objects.values('user').annotate(request_count=Count('id')).order_by('-request_count')
        
        for user in active_users:
            self.stdout.write(f"User {user['user']} made {user['request_count']} requests.")
