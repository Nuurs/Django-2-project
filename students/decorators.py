# students/decorators.py

from functools import wraps
from .models import ApiRequest
from django.utils.timezone import now

def track_api_usage(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Track the API request
        ApiRequest.objects.create(
            user=request.user,
            endpoint=request.path,
            timestamp=now()
        )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
