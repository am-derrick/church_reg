"""
module containing middleware for logging audits
"""

from django.utils.deprecation import MiddlewareMixin
from .utils import get_client_ip

class AuditLogMiddleware(MiddlewareMixin):
    """class for audit logging"""
    def process_request(self, request):
        """processes request and gets data from the headers"""
        request.audit_data = {
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')
        }
