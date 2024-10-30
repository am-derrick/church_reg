from django.utils.deprecation import MiddlewareMixin
from .utils import get_client_ip

class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.audit_data = {
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')
        }