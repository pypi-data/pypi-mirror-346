import json
from .models import UserActivity


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Don't log admin or static/media requests
        if not request.path.startswith(('/admin/', '/static/', '/media/')):
            self._log_activity(request, response)
        
        return response

    def _log_activity(self, request, response):
        # Get request data based on method
        request_data = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                request_data = request.POST.dict()
            except AttributeError:
                try:
                    request_data = json.loads(request.body.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    request_data = None

        # Determine operation type
        operation_type = None
        if request.method == 'GET':
            operation_type = 'READ'
        elif request.method == 'POST':
            operation_type = 'CREATE'
        elif request.method in ['PUT', 'PATCH']:
            operation_type = 'UPDATE'
        elif request.method == 'DELETE':
            operation_type = 'DELETE' 

        # Create activity log
        UserActivity.objects.create(
            user=request.user if request.user.is_authenticated else None,
            path=request.path,
            method=request.method,
            request_data=request_data,
            response_status=response.status_code,
            ip_address=self._get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            operation_type=operation_type
        )

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR') 